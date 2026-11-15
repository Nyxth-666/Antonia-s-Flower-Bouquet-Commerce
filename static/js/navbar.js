(function () {
var btn = document.getElementById("nav-toggle");
var menu = document.getElementById("nav-menu");
var iconOpen = document.getElementById("nav-icon-open");
var iconClose = document.getElementById("nav-icon-close");
if (!btn || !menu) return;

btn.addEventListener("click", function () {
    var isHidden = menu.classList.toggle("hidden");
    btn.setAttribute("aria-expanded", String(!isHidden));
    iconOpen.classList.toggle("hidden", !isHidden);
    iconClose.classList.toggle("hidden", isHidden);
});
})();