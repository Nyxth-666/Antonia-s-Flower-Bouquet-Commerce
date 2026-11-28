function showCartToast(message, isError) {
    let area = document.getElementById("toast-area");

    if (!area) {
        area = document.createElement("div");
        area.id = "toast-area";
        area.setAttribute("aria-live", "polite");
        area.style.cssText =
            "position:fixed;top:16px;left:50%;transform:translateX(-50%);" +
            "z-index:9999;width:min(92vw,28rem);";
        document.body.append(area);
    }

    const toast = document.createElement("div");
    toast.setAttribute("role", isError ? "alert" : "status");
    toast.style.cssText =
        "margin-bottom:8px;padding:12px 16px;border-radius:10px;" +
        "font-size:14px;font-weight:600;color:#fff;" +
        "box-shadow:0 6px 20px rgba(0,0,0,.2);" +
        `background:${isError ? "#991b1b" : "#166534"};`;
    toast.textContent = message;
    area.append(toast);

    window.setTimeout(() => {
        toast.remove();
        if (area.childElementCount === 0) area.remove();
    }, 3500);
}

function formatCartPrice(value) {
    return Number(value).toLocaleString("en-PH", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}

function updateCartView(form, result) {
    const row = form.closest("[data-cart-row]");

    if (form.matches("[data-cart-update-form]")) {
        if (result.deleted) {
            if (row) row.remove();
        } else if (row) {
            const quantity = row.querySelector("[data-cart-quantity]");
            const decrease = row.querySelector("[data-cart-decrease]");
            const increase = row.querySelector("[data-cart-increase]");

            quantity.textContent = result.quantity;
            row.querySelector("[data-cart-line-total]").textContent =
                formatCartPrice(result.line_total);
            decrease.value = result.quantity - 1;
            decrease.disabled = result.quantity <= 1;
            increase.value = result.quantity + 1;
        }
    } else if (form.matches("[data-cart-remove-form]")) {
        if (row) row.remove();
    } else if (form.matches("[data-cart-clear-form]")) {
        document.querySelectorAll("[data-cart-row]").forEach(item => item.remove());
    }

    document.querySelectorAll("[data-cart-item-count]").forEach(element => {
        element.textContent = result.item_count;
    });
    document.querySelectorAll("[data-cart-subtotal]").forEach(element => {
        element.textContent = formatCartPrice(result.subtotal);
    });

    const total = document.querySelector("[data-cart-total]");
    if (total) total.textContent = formatCartPrice(result.total);

    const itemsLabel = document.querySelector("[data-cart-items-label]");
    if (itemsLabel) {
        itemsLabel.textContent =
            `${result.item_count} Item${result.item_count === 1 ? "" : "s"}`;
    }

    const filled = document.querySelector("[data-cart-filled]");
    const empty = document.querySelector("[data-cart-empty]");
    if (filled) filled.hidden = result.empty;
    if (empty) empty.hidden = !result.empty;
}

document.addEventListener("submit", async event => {
    const form = event.target.closest(
        "[data-cart-form], [data-cart-update-form], [data-cart-remove-form], [data-cart-clear-form]"
    );
    if (!form) return;

    event.preventDefault();

    if (form.dataset.submitting === "true") return;
    form.dataset.submitting = "true";

    const buttons = Array.from(form.querySelectorAll('button[type="submit"]'));
    const originalDisabled = buttons.map(button => button.disabled);
    buttons.forEach(button => {
        button.disabled = true;
    });

    let submitter = event.submitter;
    if (!submitter && form.matches("[data-cart-update-form]")) {
        submitter = form.querySelector("[data-cart-increase]");
    }

    try {
        const formData = new FormData(form);
        if (submitter && submitter.name) {
            formData.set(submitter.name, submitter.value);
        }

        const response = await fetch(form.action, {
            method: form.method || "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json",
            },
            credentials: "same-origin",
        });

        if (response.redirected) {
            window.location.assign(response.url);
            return;
        }

        if (!response.ok) {
            throw new Error(`Add to cart failed (${response.status}).`);
        }

        const result = await response.json();
        if (!result.success) {
            throw new Error("The bouquet could not be added to your cart.");
        }

        if (form.matches("[data-cart-form]")) {
            showCartToast(result.message, false);
        } else {
            updateCartView(form, result);
            if (!form.matches("[data-cart-update-form]")) {
                showCartToast(
                    form.matches("[data-cart-clear-form]") ? "Cart cleared." : "Item removed from cart.",
                    false
                );
            }
        }
    } catch (error) {
        console.error("Could not update cart.", error);
        showCartToast("Could not update your cart. Please try again.", true);
    } finally {
        delete form.dataset.submitting;
        buttons.forEach((button, index) => {
            if (form.matches("[data-cart-update-form]")) {
                const quantity = Number(
                    form.querySelector("[data-cart-quantity]").textContent
                );
                button.disabled = button.hasAttribute("data-cart-decrease") && quantity <= 1;
            } else {
                button.disabled = originalDisabled[index];
            }
        });
    }
});
