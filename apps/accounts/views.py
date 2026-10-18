from django.shortcuts import render

PROFILE_TABS = [
    {"page": "profile",  "label": "Profile",   "template": "components/ui/cards/change-profile-card.html"},
    {"page": "orders",   "label": "My Orders", "template": "components/ui/cards/my-orders-card.html"},
    {"page": "settings", "label": "Settings",  "template": "components/ui/cards/profile-settings-card.html"},
]

SAMPLE_ORDER = [
    {"order_id": "PS-48213", "order_date": "Sep 12, 2026", "status": "Delivered",
     "item": "Medium Custom Bouquet", "price": "₱1180", "item_count": "1 item"},
    {"order_id": "PS-48214", "order_date": "Sep 12, 2026", "status": "Out for Delivery",
     "item": "Medium Custom Bouquet", "price": "₱1180", "item_count": "1 item"},
    {"order_id": "PS-48215", "order_date": "Sep 12, 2026", "status": "Confirmed",
     "item": "Medium Custom Bouquet", "price": "₱1180", "item_count": "1 item"},
    {"order_id": "PS-48215", "order_date": "Sep 12, 2026", "status": "Preparing",
    "item": "Medium Custom Bouquet", "price": "₱1180", "item_count": "1 item"},
]
STATUS_STEPS = {"Confirmed": 0, "Preparing": 1, "Out for delivery": 2, "Delivered": 3}
ORDER_STEPS = list(STATUS_STEPS)

def accounts_page(request):
    orders = [{**o, "step": STATUS_STEPS.get(o["status"], -1)} for o in SAMPLE_ORDER]
    return render(request, "accounts/accounts.html", {
        "profile_tabs": PROFILE_TABS,
        "sample_order": orders,
        "steps": ORDER_STEPS,
    })