document.addEventListener("DOMContentLoaded", () => {
    const modal = document.querySelector("#product-details-modal");

    if (!modal) return;

    const $ = selector => modal.querySelector(selector);

    const peso = amount => new Intl.NumberFormat("en-PH", {
        style: "currency",
        currency: "PHP",
        minimumFractionDigits: 2
    }).format(Number(amount) || 0);

    function openModal(card) {
        const product = card.querySelector("[data-product-details]");

        if (!product) return;

        const {
            name,
            description,
            image,
            price,
            size,
            rating,
            ratingCount,
            available
        } = product.dataset;

        $("#modal-product-name").textContent = name;
        $("#modal-product-description").textContent = description;
        $("#modal-product-price").textContent = peso(price);
        $("#modal-product-size").textContent = size || "Not specified";

        const imageElement = $("#modal-product-image");

        if (image) {
            imageElement.src = image;
            imageElement.alt = name;
            imageElement.classList.remove("hidden");
        } else {
            imageElement.removeAttribute("src");
            imageElement.alt = "No product image available";
            imageElement.classList.add("hidden");
        }

        const ratingValue = Number(rating) || 0;
        const reviewCount = Number(ratingCount) || 0;

        $("#modal-product-rating").textContent =
            reviewCount > 0
                ? `${ratingValue.toFixed(1)} (${reviewCount} reviews)`
                : "No reviews yet";

        const availability = $("#modal-product-availability");

        availability.textContent =
            available === "true" ? "Available" : "Out of stock";

        availability.className =
            available === "true"
                ? "mt-3 inline-block rounded-full bg-success/15 px-3 py-1 text-xs font-medium text-success"
                : "mt-3 inline-block rounded-full bg-error/15 px-3 py-1 text-xs font-medium text-error";

        const colorsContainer = $("#modal-product-colors");
        colorsContainer.replaceChildren();

        product.querySelectorAll("[data-color-name]").forEach(color => {
            const swatch = document.createElement("span");

            swatch.className =
                "size-5 rounded-full border border-border";

            swatch.style.backgroundColor = color.dataset.colorHex;
            swatch.title = color.dataset.colorName;
            swatch.setAttribute(
                "aria-label",
                color.dataset.colorName
            );

            colorsContainer.appendChild(swatch);
        });

        if (!colorsContainer.children.length) {
            colorsContainer.textContent = "No colors specified.";
        }

        const occasionsContainer = $("#modal-product-occasions");
        occasionsContainer.replaceChildren();

        product.querySelectorAll("[data-occasion-name]").forEach(occasion => {
            const tag = document.createElement("span");

            tag.className =
                "rounded-button border border-border px-3 py-1 text-xs text-muted";

            tag.textContent = occasion.dataset.occasionName;

            occasionsContainer.appendChild(tag);
        });

        if (!occasionsContainer.children.length) {
            occasionsContainer.textContent = "Any occasion";
        }

        $("#modal-cart-button").disabled = available !== "true";
        $("#modal-buy-button").disabled = available !== "true";

        $("#modal-cart-button").classList.toggle(
            "opacity-50",
            available !== "true"
        );

        $("#modal-buy-button").classList.toggle(
            "opacity-50",
            available !== "true"
        );

        // Show modal
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        modal.setAttribute("aria-hidden", "false");

        document.body.style.overflow = "hidden";

        modal.querySelector("[data-close-product-modal]").focus();
    }

    function closeModal() {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        modal.setAttribute("aria-hidden", "true");

        document.body.style.overflow = "";
    }

    document.addEventListener("click", event => {
        const viewButton = event.target.closest("[data-open-product-modal]");

        if (viewButton) {
            const card = viewButton.closest("article");

            if (card) openModal(card);

            return;
        }

        if (event.target.closest("[data-close-product-modal]")) {
            closeModal();
            return;
        }

        if (event.target === modal) {
            closeModal();
        }
    });

    document.addEventListener("keydown", event => {
        if (
            event.key === "Escape" &&
            !modal.classList.contains("hidden")
        ) {
            closeModal();
        }
    });
});