from datetime import datetime

from django.shortcuts import render

from apps.occasions.data.occasions import OCCASIONS
from apps.core.data.flower_meaning import FLOWER_MEANINGS

from apps.catalog.models import Bouquet


def home(request):
    now = datetime.now().astimezone()

    interval = int(now.timestamp() // 1800)

    index = interval % len(FLOWER_MEANINGS)
    featured_flower = FLOWER_MEANINGS[index]

    best_sellers = Bouquet.objects.filter(available=True).order_by("-rating")[:8]

    return render(request, "home/home.html", {
        "occasions": OCCASIONS,
        "flower": featured_flower,
        "best_sellers": best_sellers,
    })