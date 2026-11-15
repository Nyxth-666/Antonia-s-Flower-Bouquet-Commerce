document.addEventListener("DOMContentLoaded", () => {

    const $ = (selector, parent = document) =>
        parent.querySelector(selector);

    const $$ = (selector, parent = document) =>
        [...parent.querySelectorAll(selector)];

    const form = $("#bouquet");
    const preview = $("#bouquet-preview");

    if (!form || !preview) return;

    const peso = amount =>
        new Intl.NumberFormat("en-PH", {
            style: "currency",
            currency: "PHP",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);

    const money = value => Number(value) || 0;

    const state = {
        size: null,
        flowers: {},
        color: null,
        wrapping: null,
        addons: new Set()
    };

    $$("[data-flower-option]").forEach(flower => {
        state.flowers[flower.dataset.flowerId] = 0;
    });

    function selectOption(container, selectedButton) {
        $$(".option-selected", container).forEach(button => {
            button.classList.remove("option-selected");
        });

        $$("button", container).forEach(button => {
            const active = button === selectedButton;

            button.setAttribute("aria-pressed", String(active));

            button.classList.toggle(
                "option-selected",
                active
            );
        });

        selectedButton.classList.add("option-selected");
    }

    function getSelected(containerId) {
        return $(
            `#${containerId} button[aria-pressed="true"]`
        );
    }

    function calculatePrices() {
        const selectedSize = getSelected("size-options");

        const base = money(
            selectedSize?.dataset.basePrice
        );

        const flowerTotal = $$("[data-flower-option]")
            .reduce((total, flower) => {
                const quantity = state.flowers[
                    flower.dataset.flowerId
                ] || 0;

                const price = money(
                    flower.dataset.flowerPrice
                );

                return total + quantity * price;
            }, 0);

        const selectedWrapping = getSelected(
            "wrapping-options"
        );

        const wrappingTotal = money(
            selectedWrapping?.dataset.wrappingPrice
        );

        const addonTotal = $$(
            "#addon-options button[aria-pressed='true']"
        ).reduce((total, addon) => {
            return total + money(addon.dataset.addonPrice);
        }, 0);

        return {
            base,
            flowers: flowerTotal,
            wrapping: wrappingTotal,
            addons: addonTotal,
            total: base + flowerTotal +
                wrappingTotal + addonTotal
        };
    }

    function updatePrices() {
        const prices = calculatePrices();

        const selectedSize = getSelected("size-options");

        $('[data-out="size"]').textContent =
            selectedSize
                ? `Base (${selectedSize.dataset.sizeName})`
                : "Base (Not selected)";

        $('[data-out="base"]').textContent =
            peso(prices.base);

        $('[data-out="fl"]').textContent =
            peso(prices.flowers);

        $('[data-out="wr"]').textContent =
            peso(prices.wrapping);

        $('[data-out="ad"]').textContent =
            peso(prices.addons);

        $('[data-out="total"]').textContent =
            peso(prices.total);

        return prices;
    }

    function updateQuantity(flower, amount) {
        const flowerId = flower.dataset.flowerId;

        const currentQuantity = state.flowers[flowerId] || 0;

        const newQuantity = Math.max(
            0,
            Math.min(99, currentQuantity + amount)
        );

        state.flowers[flowerId] = newQuantity;

        $("[data-quantity]", flower).textContent =
            newQuantity;
    }

    function createFlower(x, y, color, index) {
        const rotation = (index * 37) % 360;

        return `
            <g transform="translate(${x} ${y}) rotate(${rotation})">
                ${Array.from({ length: 8 }, (_, i) => {
                    const angle = i * 45;

                    return `
                        <ellipse
                            cx="0"
                            cy="-11"
                            rx="7"
                            ry="11"
                            fill="${color}"
                            transform="rotate(${angle})"
                        />
                    `;
                }).join("")}

                <circle
                    cx="0"
                    cy="0"
                    r="5"
                    fill="#D8A45E"
                />
            </g>
        `;
    }

    function renderPreview() {
        const selectedFlowers = $$("[data-flower-option]")
            .flatMap(flower => {
                const quantity = state.flowers[
                    flower.dataset.flowerId
                ] || 0;

                return Array.from(
                    { length: quantity },
                    () => flower.dataset.flowerName
                );
            });

        const wrapping = getSelected("wrapping-options");
        const color = getSelected("color-options");

        const wrappingColor =
            color?.dataset.colorHex || "#D8C5A5";

        const visibleFlowers = selectedFlowers.slice(0, 24);

        const flowerPositions = [
            [100, 95], [140, 65], [180, 65],
            [220, 95], [120, 125], [160, 115],
            [200, 125], [80, 130], [240, 130],
            [140, 155], [180, 155], [110, 90],
            [210, 90], [160, 45], [130, 105],
            [190, 105], [95, 115], [225, 115],
            [145, 85], [175, 85], [125, 140],
            [195, 140], [160, 145], [160, 95]
        ];

        const flowersSVG = visibleFlowers.map(
            (flower, index) => {
                const [x, y] = flowerPositions[index];

                return createFlower(
                    x,
                    y,
                    "#D58A9B",
                    index
                );
            }
        ).join("");

        const stemsSVG = visibleFlowers.map(
            (_, index) => {
                const [x, y] = flowerPositions[index];

                return `
                    <path
                        d="M160 225 Q${x} 190 ${x} ${y + 10}"
                        stroke="#63805B"
                        stroke-width="3"
                        fill="none"
                    />
                `;
            }
        ).join("");

        preview.innerHTML = `
            <div class="flex w-full flex-col items-center gap-3">
                <svg
                    viewBox="0 0 320 300"
                    class="w-full max-w-[340px]"
                    role="img"
                    aria-label="Your customized bouquet preview"
                >
                    ${stemsSVG}

                    <g fill="#718D60">
                        <path d="M145 190 Q105 155 100 170 Q120 195 145 190"/>
                        <path d="M175 190 Q215 155 220 170 Q200 195 175 190"/>
                        <path d="M155 205 Q125 185 120 200 Q140 215 155 205"/>
                    </g>

                    ${flowersSVG}

                    <path
                        d="M95 190 Q160 215 225 190
                           L205 275 L115 275 Z"
                        fill="${wrappingColor}"
                        stroke="#A58B6B"
                        stroke-width="2"
                    />

                    <path
                        d="M95 190 Q160 207 225 190"
                        stroke="#A58B6B"
                        stroke-width="3"
                        fill="none"
                    />

                    <path
                        d="M150 207 L160 220 L170 207"
                        fill="none"
                        stroke="#A66A59"
                        stroke-width="4"
                    />
                </svg>

                <p class="text-xs text-muted">
                    ${visibleFlowers.length} flower(s) displayed
                    ${wrapping ? ` · ${wrapping.dataset.wrappingName}` : ""}
                </p>
            </div>
        `;

        if (visibleFlowers.length === 0) {
            preview.innerHTML = `
                <p class="text-sm text-muted">
                    Select flowers to build your bouquet.
                </p>
            `;
        }
    }

    function updateConfig() {
        const selectedSize = getSelected("size-options");
        const selectedColor = getSelected("color-options");
        const selectedWrapping = getSelected(
            "wrapping-options"
        );

        const selectedAddons = $$(
            "#addon-options button[aria-pressed='true']"
        );

        const config = {
            size_id: selectedSize?.dataset.sizeId || null,

            flowers: Object.entries(state.flowers)
                .filter(([, quantity]) => quantity > 0)
                .map(([flowerId, quantity]) => ({
                    flower_option_id: Number(flowerId),
                    quantity
                })),

            color_id: selectedColor?.dataset.colorId || null,

            wrapping_id:
                selectedWrapping?.dataset.wrappingId || null,

            addon_ids: selectedAddons.map(
                addon => Number(addon.dataset.addonId)
            )
        };

        $("#config").value = JSON.stringify(config);
    }

    function update() {
        updatePrices();
        renderPreview();
        updateConfig();
    }

    form.addEventListener("click", event => {
        const button = event.target.closest("button");

        if (!button || !form.contains(button)) return;

        if (
            button.matches(
                "[data-quantity-increase], [data-quantity-decrease]"
            )
        ) {
            const flower = button.closest(
                "[data-flower-option]"
            );

            if (!flower) return;

            const amount = button.hasAttribute(
                "data-quantity-increase"
            ) ? 1 : -1;

            updateQuantity(flower, amount);
        }

        else if (button.matches("[data-size-id]")) {
            selectOption($("#size-options"), button);
        }

        else if (button.matches("[data-color-id]")) {
            selectOption($("#color-options"), button);
        }

        else if (button.matches("[data-wrapping-id]")) {
            selectOption($("#wrapping-options"), button);
        }

        else if (button.matches("[data-addon-id]")) {
            const active =
                button.getAttribute("aria-pressed") === "true";

            button.setAttribute(
                "aria-pressed",
                String(!active)
            );

            button.classList.toggle(
                "option-selected",
                !active
            );
        } else {
            return;
        }

        update();
    });

    $("#msg")?.addEventListener("input", event => {
        $("#cnt").textContent = event.target.value.length;
    });

    const firstSize = $("#size-options button");

    if (firstSize) {
        selectOption($("#size-options"), firstSize);
    }

    update();
});