from django.contrib import admin
from django.urls import reverse_lazy

EXCLUDED_APPS = {"auth"}

# Icons use Google Material Symbols names, which Unfold renders from its bundled font.
# Fallback for models without an explicit entry.
DEFAULT_MODEL_ICON = "table_chart"

MODEL_ICONS = {
    "accounts.Admin": "admin_panel_settings",
    "accounts.Customer": "group",
    "catalog.ArrangementType": "category",
    "catalog.Bouquet": "local_florist",
    "catalog.Color": "palette",
    "catalog.FlowerType": "yard",
    "catalog.Occasion": "celebration",
    "contact.Entry": "contact_mail",
    "customization.AddOn": "extension",
    "customization.BouquetSize": "straighten",
    "customization.CustomBouquet": "design_services",
    "customization.FlowerOption": "spa",
    "customization.WrappingOption": "card_giftcard",
    "orders.CartItem": "shopping_basket",
    "orders.Cart": "shopping_cart",
    "orders.CustomCartItem": "shopping_cart_checkout",
}

MY_PROFILE_SECTION = {
    "title": "My Profile",
    "separator": False,
    "collapsible": False,
    "items": [
        {"title": "Profile", "icon": "account_circle", "link": reverse_lazy("admin_profile")},
        {"title": "Settings", "icon": "settings", "link": reverse_lazy("admin_settings")},
        {"title": "Product", "icon": "inventory_2", "link": reverse_lazy("admin_product")},
    ],
}


def model_icon(app_label, object_name):
    return MODEL_ICONS.get(f"{app_label}.{object_name}", DEFAULT_MODEL_ICON)


def navigation(request=None):
    sections = [MY_PROFILE_SECTION]
    for app in admin.site.get_app_list(request):
        if app["app_label"] in EXCLUDED_APPS:
            continue
        sections.append({
            "title": app["name"],
            "separator": True,
            "collapsible": False,
            "items": [
                {
                    "title": m["name"],
                    "icon": model_icon(app["app_label"], m["object_name"]),
                    "link": m["admin_url"],
                }
                for m in app["models"]
            ],
        })
    return sections