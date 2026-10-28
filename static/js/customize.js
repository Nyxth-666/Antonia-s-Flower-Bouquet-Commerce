
document.addEventListener("DOMContentLoaded", () => {
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];

  const peso = amount => new Intl.NumberFormat("en-PH", {
    style: "currency",
    currency: "PHP",
    maximumFractionDigits: 0
  }).format(amount);

  const num = value => Number(String(value ?? "").replace(/[^\d.-]/g, "")) || 0;

  const BASE = {
    Small: 500,
    Medium: 650,
    Large: 800,
    "Extra Large": 1000
  };

  const FLOWERS = [
    // Fresh flowers
    ["Anthuriums", 55],
    ["Asters", 55],
    ["Baby's Breath", 40, "bunch"],
    ["Carnation", 65],
    ["Daisies", 45],
    ["Gerberas", 55],
    ["Goldenrod", 55],
    ["Lilies", 45],
    ["Lisianthus/Paper Roses", 30],
    ["Mixed Flowers", 55],
    ["Roses", 55],
    ["Sunflower", 55],
    ["Tulips", 55],

    // Artificial, dried and decorative
    ["Artificial Flowers", 40],
    ["Decorative Flowers", 35],
    ["Decorative Roses", 45],
    ["Dried Flowers", 45],

    // Chocolates and money
    ["Chocolate", 25, "piece"],
    ["Chocolate Bouquet", 350, "bouquet"],
    ["Money Rose", 100, "piece"],
    ["Money Bouquet", 300, "bouquet"],
  ];

  const COLORS = [
    ["Rose", "rose"],
    ["Blush", "blush"],
    ["Gold", "gold"],
    ["Sage", "sage"],
    ["Ivory", "ivory"]
  ];

  const WRAPS = [
    ["Kraft paper", 0, "kraft"],
    ["White paper", 0, "white"],
    ["Satin wrap", 60, "sage"],
    ["Luxury box", 150, "wine"]
  ];

  const focus = "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent";
  const quantityButton = `flex size-5 shrink-0 cursor-pointer items-center justify-center rounded-full border border-border text-[13px] text-muted transition hover:border-accent hover:text-accent ${focus}`;

  function render(selector, items, template) {
    $(selector).innerHTML = items.map(template).join("");
  }

  function renderFlowers() {
    render("#flowers", FLOWERS, ([name, price, unit = "stem"]) => `
      <div data-flower="${name}" data-price="${price}"
        class="flex min-w-0 items-center gap-2.5 rounded-xl border border-border px-3 py-3 sm:gap-3.5 sm:pl-7 sm:pr-[22px]">
        <span class="size-4 shrink-0 rounded-full bg-[#c48aa0]"></span>

        <p class="min-w-0 flex-1 text-[13px] font-semibold text-foreground sm:text-[15px]">
          ${name}
          <span class="block text-[12px] font-normal text-muted">₱${price} / ${unit}</span>
        </p>

        <div class="flex shrink-0 items-center gap-1.5 sm:gap-2.5">
          <button type="button" data-step="-1"
            aria-label="Remove ${name}" class="${quantityButton}">−</button>
          <output class="w-4 text-center text-[13px]">0</output>
          <button type="button" data-step="1"
            aria-label="Add ${name}" class="${quantityButton}">+</button>
        </div>
      </div>
    `);
  }

  function renderColors() {
    render("#colors", COLORS, ([name, color]) => `
      <button type="button" data-color="${name}"
        aria-label="${name} wrapping" title="${name}"
        aria-pressed="false"
        class="color-swatch color-${color} ${focus}">
      </button>
    `);
  }

  function renderWraps() {
    render("#wraps", WRAPS, ([name, price, color]) => `
      <button type="button" data-wrap="${name}" data-price="${price}"
        aria-pressed="false"
        class="wrap-button cursor-pointer rounded-xl border border-border px-2 py-1.5 text-center text-[12px] text-muted transition hover:border-accent hover:text-accent sm:px-3.5 sm:text-[15px] ${focus}">
        <span class="wrap-preview wrap-${color}"></span>
        ${name}
      </button>
    `);
  }

  function selectOption(selector, selected) {
    $$(selector).forEach(button => {
      const active = button === selected;
      button.setAttribute("aria-pressed", String(active));

      if (selector === "[data-color]") {
        button.classList.toggle("selected-color", active);
      } else {
        button.classList.toggle("bg-secondary", active);
        button.classList.toggle("border-secondary", active);
        button.classList.toggle("text-soft-white", active);
        button.classList.toggle("border-border", !active);
        button.classList.toggle("text-muted", !active);
      }
    });
  }

  function selected(selector) {
    return $(`${selector}[aria-pressed="true"]`);
  }

  function update() {
    const size = selected("[data-size]")?.dataset.size || "Large";
    const wrap = selected("[data-wrap]");
    const flowers = $$("[data-flower]");
    const addons = $$('[data-addon][aria-pressed="true"]');

    const base = BASE[size];

    const flowerTotal = flowers.reduce((total, flower) => {
      const quantity = Number(flower.querySelector("output").textContent) || 0;
      return total + Number(flower.dataset.price) * quantity;
    }, 0);

    const wrapTotal = num(wrap?.dataset.price);
    const addonTotal = addons.reduce(
      (total, addon) => total + num(addon.dataset.price),
      0
    );

    const totals = {
      base,
      fl: flowerTotal,
      wr: wrapTotal,
      ad: addonTotal,
      total: base + flowerTotal + wrapTotal + addonTotal
    };

    Object.entries(totals).forEach(([key, value]) => {
      $(`[data-out="${key}"]`).textContent = peso(value);
    });

    $('[data-out="size"]').textContent = `Base (${size})`;

    $("#config").value = JSON.stringify({
      size,
      flowers: Object.fromEntries(
        flowers
          .map(flower => [
            flower.dataset.flower,
            Number(flower.querySelector("output").textContent) || 0
          ])
          .filter(([, quantity]) => quantity > 0)
      ),
      color: selected("[data-color]")?.dataset.color || null,
      wrap: wrap?.dataset.wrap || null,
      addons: addons.map(addon => addon.dataset.addon)
    });
  }

  $("#bouquet").addEventListener("click", event => {
    const button = event.target.closest("button");
    if (!button) return;

    if (button.dataset.step) {
      const flower = button.closest("[data-flower]");
      const output = flower.querySelector("output");
      const quantity = Number(output.textContent) + Number(button.dataset.step);

      output.textContent = Math.max(0, Math.min(99, quantity));
    } else if (button.matches("[data-size]")) {
      selectOption("[data-size]", button);
    } else if (button.matches("[data-color]")) {
      selectOption("[data-color]", button);
    } else if (button.matches("[data-wrap]")) {
      selectOption("[data-wrap]", button);
    } else if (button.matches("[data-addon]")) {
      const active = button.getAttribute("aria-pressed") === "true";
      button.setAttribute("aria-pressed", String(!active));

      button.classList.toggle("bg-secondary", !active);
      button.classList.toggle("border-secondary", !active);
      button.classList.toggle("text-soft-white", !active);
      button.classList.toggle("border-border", active);
      button.classList.toggle("text-muted", active);
    } else {
      return;
    }

    update();
  });

  $("#msg").addEventListener("input", event => {
    $("#cnt").textContent = event.target.value.length;
  });

  renderFlowers();
  renderColors();
  renderWraps();

  selectOption("[data-size]", $('[data-size="Large"]'));
  selectOption("[data-color]", $('[data-color="Rose"]'));

  update();
});
