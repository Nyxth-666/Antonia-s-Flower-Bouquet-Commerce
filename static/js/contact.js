// static/js/contact.js
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contact-form");
    if (!form) return;

    form.addEventListener("submit", () => {
        const button = form.querySelector("button[type='submit']");
        button.disabled = true;
        button.textContent = "Sending...";
    });
});