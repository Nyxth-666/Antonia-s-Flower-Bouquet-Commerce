from datetime import datetime

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