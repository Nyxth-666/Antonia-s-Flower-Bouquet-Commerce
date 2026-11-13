from datetime import datetime

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from apps.catalog.models import Occasion, Bouquet
from apps.core.data.flower_meaning import FLOWER_MEANINGS


def home(request):
    now = datetime.now().astimezone()

    interval = int(now.timestamp() // 1800)

    index = interval % len(FLOWER_MEANINGS)
    featured_flower = FLOWER_MEANINGS[index]

    best_sellers = Bouquet.objects.filter(available=True).order_by("-rating")[:8]

    occasions = Occasion.objects.filter(is_active=True)

    return render(request, "home/home.html", {
        "occasions": occasions,
        "flower": featured_flower,
         "best_sellers": best_sellers,
    })

# admin page
@staff_member_required
def profile(request):
    return render(request, "admin/admin-profile.html", {**admin.site.each_context(request), "title": "My Profile"})

@staff_member_required
def profile_settings(request):
    return render(request, "admin/admin-settings.html", {**admin.site.each_context(request), "title": "Profile Settings"})

@staff_member_required
def product(request):
    return render(request, "admin/admin-products.html", {**admin.site.each_context(request), "title": "Products"}) 
