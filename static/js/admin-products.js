document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("product-form-modal");
    const form = document.getElementById("product-form");
    if (!modal || !form) return;

    const field = (name) => form.querySelector(`[name="${name}"]`);
    const radios = [...form.querySelectorAll('[name="available"]')];

    function toggle(open) {
        modal.classList.toggle("hidden", !open);
        modal.classList.toggle("grid", open);
        modal.setAttribute("aria-hidden", String(!open));
        document.body.style.overflow = open ? "hidden" : "";
    }

    function openModal(data) {
        const title = document.getElementById("product-form-title");
        if (title) title.textContent = data ? "Edit Product" : "Add Product";

        form.reset();
        field("product_id").value = data?.id || "";
        field("name").value = data?.name || "";
        field("description").value = data?.description || "";
        field("price").value = data?.price || "";
        field("quantity").value = data?.quantity || "0";
        field("size").value = data?.size || "";
        field("arrangement_type").value = data?.arrangement || "";
        radios.forEach((radio) => (radio.checked = radio.value === (data ? data.available : "true")));

        toggle(true);
        field("name").focus();
    }

    document.addEventListener("click", (event) => {
        const edit = event.target.closest("[data-edit-product]");
        if (event.target.closest("[data-add-product]")) return openModal();
        if (edit) return openModal(edit.dataset);
        if (event.target.closest("[data-close-product-modal]") || event.target === modal) toggle(false);
    });

    document.addEventListener("keydown", (event) => event.key === "Escape" && toggle(false));

    // Modal rendered open by the server (failed submit) still needs the scroll lock.
    if (!modal.classList.contains("hidden")) document.body.style.overflow = "hidden";

    document.querySelectorAll("[data-confirm]").forEach((button) =>
        button.addEventListener("click", (event) => {
            if (!window.confirm(button.dataset.confirm)) event.preventDefault();
        })
    );
});
