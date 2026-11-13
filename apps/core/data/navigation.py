from django.contrib import admin
from django.urls import reverse_lazy

EXCLUDED_APPS = {"auth"}

MY_PROFILE_SECTION = {
    "title": "My Profile",
    "separator": False,
    "collapsible": False,
    "items": [
        {"title": "Profile", "icon": "dashboard", "link": reverse_lazy("admin_profile")},
        {"title": "Settings", "icon": "people", "link": reverse_lazy("admin_settings")},
        {"title": "Product", "icon": "box", "link": reverse_lazy("admin_product")},
    ],
}

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
                {"title": m["name"], "icon": "table_chart", "link": m["admin_url"]}
                for m in app["models"]
            ],
        })
    return sections