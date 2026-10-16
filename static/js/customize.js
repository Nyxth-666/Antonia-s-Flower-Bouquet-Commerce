
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const peso = (amount) =>
  new Intl.NumberFormat("en-PH", {
    style: "currency",
    currency: "PHP",
    maximumFractionDigits: 0,
  }).format(amount);

const num = (value) =>
  Number(String(value ?? "").replace(/[^\d.-]/g, "")) || 0;

const BASE = {
  Small: 500,
  Medium: 650,
  Large: 800,
  "Extra Large": 1000,
};

// Example prices. Change these to your actual prices.
const FLOWERS = [
  ["Lisianthus/Paper Roses", 55],
  ["Tulips", 55],
  ["Lillies", 55],
  ["Carnation", 55],
  ["Sunflower", 65],
  ["Gerberas", 50],
  ["Roses", 60],
  ["Mixed flowers", 75],
];

const COLORS = [
  ["Rose", "rose"],
  ["Blush", "blush"],
  ["Gold", "gold"],
  ["Sage", "sage"],
  ["Ivory", "ivory"],
];

const WRAPS = [
  ["Kraft paper", 0, "kraft"],
  ["White paper", 0, "white"],
  ["Satin wrap", 60, "sage"],
  ["Luxury box", 150, "wine"],
];

const FOCUS =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent";

const QB = `quantity-button ${FOCUS}`;

function render(selector, items, template) {
  const container = $(selector);

  if (container) {
    container.innerHTML = items.map(template).join("");
  } else {
    console.error(`Customization element not found: ${selector}`);
  }
}

// Render all eight flower cards.
render("#flowers", FLOWERS, ([name, price]) => `
  <div data-flower="${name}" data-price="${price}" class="flower-card">

    <span class="flower-dot" aria-hidden="true"></span>

    <p class="flower-details">
      <span class="flower-name">${name}</span>
      <span class="flower-price">₱${price} / stem</span>
    </p>

    <div class="quantity-controls">
      <button type="button"
              data-step="-1"
              aria-label="Remove one ${name}"
              class="${QB}">−</button>

      <output class="quantity-value" aria-live="polite">0</output>

      <button type="button"
              data-step="1"
              aria-label="Add one ${name}"
              class="${QB}">+</button>
    </div>

  </div>
`);

// Render wrapping colors.
render("#colors", COLORS, ([name, color]) => `
  <button type="button"
          data-color="${name}"
          aria-label="${name} wrapping color"
          title="${name}"
          aria-pressed="false"
          class="color-swatch color-${color} ${FOCUS}">
  </button>
`);

// Render wrapping options.
render("#wraps", WRAPS, ([name, price, color]) => `
  <button type="button"
          data-wrap="${name}"
          data-price="${price}"
          aria-pressed="false"
          class="wrap-option ${FOCUS}">

    <span class="wrap-preview wrap-${color}"></span>
    <span>${name}</span>
    <span class="wrap-price">${peso(price)}</span>

  </button>
`);

function selectOption(selector, active) {
  $$(selector).forEach((element) => {
    const selected = element === active;

    element.setAttribute("aria-pressed", String(selected));

    if (selector === "[data-color]") {
      element.classList.toggle("selected-color", selected);
    } else {
      element.classList.toggle("selected-option", selected);
    }
  });
}

function update() {
  const size =
    $('[data-size][aria-pressed="true"]')?.dataset.size || "Large";

  const selectedWrap = $('[data-wrap][aria-pressed="true"]');
  const flowerRows = $$("[data-flower]");
  const selectedAddons = $$('[data-addon][aria-pressed="true"]');

  const base = BASE[size];

  const flowersTotal = flowerRows.reduce((sum, row) => {
    const price = Number(row.dataset.price);
    const quantity = Number(row.querySelector("output").textContent);

    return sum + price * quantity;
  }, 0);

  const wrappingTotal = num(selectedWrap?.dataset.price);

  const addonsTotal = selectedAddons.reduce((sum, addon) => {
    return sum + num(addon.dataset.price);
  }, 0);

  const totals = {
    base,
    fl: flowersTotal,
    wr: wrappingTotal,
    ad: addonsTotal,
    total: base + flowersTotal + wrappingTotal + addonsTotal,
  };

  Object.entries(totals).forEach(([key, value]) => {
    const output = $(`[data-out="${key}"]`);

    if (output) {
      output.textContent = peso(value);
    }
  });

  const sizeOutput = $('[data-out="size"]');

  if (sizeOutput) {
    sizeOutput.textContent = `Base (${size})`;
  }

  // Save the customization in the hidden form field.
  $("#config").value = JSON.stringify({
    size,
    flowers: Object.fromEntries(
      flowerRows
        .map((row) => [
          row.dataset.flower,
          Number(row.querySelector("output").textContent),
        ])
        .filter(([, quantity]) => quantity > 0)
    ),
    color:
      $('[data-color][aria-pressed="true"]')?.dataset.color || null,
    wrap: selectedWrap?.dataset.wrap || null,
    addons: selectedAddons.map((addon) => addon.dataset.addon),
    prices: totals,
  });
}

// Handle clicks on customization options.
$("#bouquet").addEventListener("click", (event) => {
  const button = event.target.closest("button");

  if (!button) return;

  if (button.dataset.step !== undefined) {
    const row = button.closest("[data-flower]");
    const output = row.querySelector("output");

    const current = Number(output.textContent);
    const step = Number(button.dataset.step);

    output.textContent = Math.max(
      0,
      Math.min(99, current + step)
    );
  } else if (button.dataset.size) {
    selectOption("[data-size]", button);
  } else if (button.dataset.color) {
    selectOption("[data-color]", button);
  } else if (button.dataset.wrap) {
    selectOption("[data-wrap]", button);
  } else if (button.dataset.addon) {
    const selected =
      button.getAttribute("aria-pressed") === "true";

    button.setAttribute("aria-pressed", String(!selected));
    button.classList.toggle("selected-option", !selected);
  } else {
    return;
  }

  update();
});

// Message character counter.
$("#msg").addEventListener("input", (event) => {
  $("#cnt").textContent = event.target.value.length;
});

// Initial selections and prices.
selectOption("[data-size]", $('[data-size="Large"]'));
selectOption("[data-color]", $('[data-color="Rose"]'));

update();
