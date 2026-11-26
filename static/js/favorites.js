function playAnimation(element, keyframes, options) {
    if (typeof element.animate !== "function") return Promise.resolve();

    return new Promise(resolve => {
        const animation = element.animate(keyframes, options);
        animation.addEventListener("finish", resolve, { once: true });
        animation.addEventListener("cancel", resolve, { once: true });
    });
}

document.addEventListener("submit", async event => {
    const form = event.target.closest("[data-favorite-form]");

    if (!form) return;

    event.preventDefault();

    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) submitButton.disabled = true;

    try {
        const response = await fetch(form.action, {
            method: form.method || "POST",
            body: new FormData(form),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            credentials: "same-origin",
        });

        if (!response.ok) {
            throw new Error(`Favorite request failed (${response.status}).`);
        }

        const result = await response.json();
        const bouquetId = String(result.bouquet_id);
        const bouquetName = form.dataset.bouquetName || "bouquet";

        document.querySelectorAll("[data-favorite-form]").forEach(favoriteForm => {
            if (favoriteForm.dataset.bouquetId !== bouquetId) return;

            const button = favoriteForm.querySelector("[data-favorite-button]");
            if (!button) return;

            const isFavorite = result.is_favorite;
            button.classList.toggle("text-primary", !isFavorite);
            button.style.color = isFavorite ? "rgba(221, 88, 88, 1)" : "";
            button.setAttribute(
                "aria-label",
                `${isFavorite ? "Remove" : "Add"} ${favoriteForm.dataset.bouquetName || bouquetName} from favorites`
            );
            button.title = isFavorite ? "Remove from favorites" : "Add to favorites";

            const icon = button.querySelector("svg");
            if (icon) {
                icon.setAttribute("fill", isFavorite ? "currentColor" : "none");
            }
        });

        const product = document.querySelector(
            `[data-product-details][data-id="${bouquetId}"]`
        );
        if (product) product.dataset.favorite = String(result.is_favorite);

        const modalButton = document.querySelector("#modal-favorite-button");
        const modalForm = modalButton && modalButton.closest("[data-favorite-form]");
        if (modalButton && modalForm && modalForm.dataset.bouquetId === bouquetId) {
            modalButton.textContent = result.is_favorite ? "Remove from Favorites" : "Favorite";
            modalButton.className = result.is_favorite
                ? "flex-1 rounded-button border border-primary px-4 py-3 text-sm font-medium text-primary transition hover:bg-primary hover:text-soft-white"
                : "flex-1 rounded-button bg-primary px-4 py-3 text-sm font-medium text-soft-white transition hover:opacity-90";
        }

        if (!result.is_favorite) {
            const card = document.querySelector(
                `[data-favorite-card][data-bouquet-id="${bouquetId}"]`
            );
            if (card) {
                const prefersReducedMotion =
                    window.matchMedia &&
                    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
                if (!prefersReducedMotion) {
                    const heart = card.querySelector("[data-favorite-button] svg");
                    if (heart) {
                        await playAnimation(
                            heart,
                            [
                                { transform: "scale(1)" },
                                { transform: "scale(0.75)" },
                                { transform: "scale(1)" },
                            ],
                            { duration: 180, easing: "ease-in-out" }
                        );
                    }

                    await playAnimation(
                        card,
                        [
                            { opacity: 1, transform: "scale(1)" },
                            { opacity: 0, transform: "scale(0.96)" },
                        ],
                        { duration: 220, easing: "ease-in", fill: "forwards" }
                    );
                }

                card.remove();
                const remaining = document.querySelectorAll("[data-favorite-card]").length;
                const count = document.querySelector("[data-favorites-count]");
                const grid = document.querySelector("[data-favorites-grid]");
                const emptyState = document.querySelector("[data-favorites-empty]");

                if (count) {
                    count.textContent = `${remaining} saved bouquet${remaining === 1 ? "" : "s"}`;
                }

                if (remaining === 0) {
                    if (grid) grid.classList.add("hidden");
                    if (emptyState) emptyState.classList.remove("hidden");
                }
            }
        }
    } catch (error) {
        console.error("Could not update favorite.", error);
        window.alert("Could not update your favorite. Please try again.");
    } finally {
        if (submitButton) submitButton.disabled = false;
    }
});
