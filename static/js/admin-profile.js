document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("profile-form");
    const button = document.getElementById("profile-edit-btn");
    if (!form || !button) return;

    const fields = [...form.querySelectorAll('input[name="full_name"], input[name="email"], input[name="phone"]')];
    if (!fields.length) return;

    const hasErrors = form.dataset.editing === "true";
    let editing = hasErrors;
    const isDirty = () => fields.some((field) => field.value !== field.defaultValue);
    const updateButton = () => (button.textContent = editing && (isDirty() || hasErrors) ? "Save" : "Edit Profile");
    const setEditing = (enabled) => {
        editing = enabled;
        fields.forEach((field) => (field.readOnly = !enabled));
        updateButton();
    };

    form.addEventListener("input", updateButton);
    button.addEventListener("click", () => {
        if (!editing) {
            setEditing(true);
            fields[0].focus();
        } else if (isDirty() || hasErrors) form.requestSubmit();
        else setEditing(false);
    });
    form.addEventListener("submit", (event) => { if (!editing || (!isDirty() && !hasErrors)) event.preventDefault(); });
    setEditing(editing);
});
