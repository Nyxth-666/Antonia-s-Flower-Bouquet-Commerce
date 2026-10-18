from django.shortcuts import render
from django.http import HttpRequest

PROFILE_TABS = [
    {"page": "profile",  "label": "Profile",   "template": "components/ui/cards/change-profile-card.html"},
    {"page": "orders",   "label": "My Orders", "template": "components/ui/cards/my-orders-card.html"},
    {"page": "settings", "label": "Settings",  "template": "components/ui/cards/profile-settings-card.html"},
]

def accounts_page(request):
    return render(request, "accounts/accounts.html", {"profile_tabs": PROFILE_TABS})