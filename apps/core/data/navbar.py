
NAVBAR_LINKS = [
    {
        "name": "Home",
        "url": "core:home",
    },
    {
        "name": "Shop",
        "url": "catalog:catalog",
    },
    {
        "name": "Occasions",
        "url": "occasions:occasions",
        "dropdown": True,
    },
    {
        "name": "By Types",
        "url": "catalog:catalog",
        "dropdown": True,
    },
    {
        "name": "Customize",
        "url": "customization:customization",
    },
    {
        "name": "About",
        "url": "about:about",
    },
    {
        "name": "Contact",
        "url": "contact:contact",
    },
]

NAVBAR_ICONS = [
    {
        "name": "Profile",
        "icon_template": "components/ui/icons/user_icon.html",
        "url": "accounts:accounts",
    },
    {
        "name": "Favorites",
        "icon_template": "components/ui/icons/heart_icon.html",
        "url": "favorites:favorites",
    },
    {
        "name": "Cart",
        "icon_template": "components/ui/icons/cart_icon.html",
        "url": "orders:orders",
    },
]

NAVBAR_SEARCH = {
    "placeholder": "Search flowers here...",
    "url": "catalog:catalog",
    "parameter": "q",
}