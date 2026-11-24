document.addEventListener("DOMContentLoaded", () => {
    const tabs = [...document.querySelectorAll("[data-chart-tab]")];
    const panels = [...document.querySelectorAll("[data-chart-panel]")];
    if (!tabs.length || !panels.length) return;

    function activate(name) {
        tabs.forEach((tab) => {
            const active = tab.dataset.chartTab === name;
            tab.setAttribute("aria-selected", String(active));
            tab.classList.toggle("bg-secondary", active);
            tab.classList.toggle("text-white", active);
            tab.classList.toggle("text-muted", !active);
            tab.classList.toggle("hover:text-foreground", !active);
        });

        panels.forEach((panel) => {
            panel.classList.toggle("hidden", panel.dataset.chartPanel !== name);
        });
    }

    tabs.forEach((tab) => {
        tab.addEventListener("click", () => activate(tab.dataset.chartTab));
    });
});
