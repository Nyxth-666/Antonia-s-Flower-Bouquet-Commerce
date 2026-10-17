from django.shortcuts import render
from django.http import HttpRequest

PROFILE_TABS = [
    {"page": "profile",  "label": "Profile",   "template": "accounts/profile.html"},
    {"page": "orders",   "label": "My Orders", "template": "accounts/my-orders.html"},
    {"page": "settings", "label": "Settings",  "template": "accounts/settings.html"},
]

def accounts_page(request):
    return render(request, "accounts/accounts.html", {"profile_tabs": PROFILE_TABS})