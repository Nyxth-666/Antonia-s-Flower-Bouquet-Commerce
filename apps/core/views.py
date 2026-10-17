from datetime import datetime

from django.shortcuts import render

from apps.occasions.data.occasions import OCCASIONS
from apps.core.data.flower_meaning import FLOWER_MEANINGS


def home(request):
    now = datetime.now().astimezone()

    interval = int(now.timestamp() // 1800)

    index = interval % len(FLOWER_MEANINGS)
    featured_flower = FLOWER_MEANINGS[index]

    return render(request, "home/home.html", {
        "occasions": OCCASIONS,
        "flower": featured_flower,
    })