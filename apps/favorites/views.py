from django.shortcuts import render
from apps.catalog.models import Bouquet

def favorites(request):
    # Temporary, for frontend preview only
    if request.GET.get("empty"):
        items = []
    else:
        items = Bouquet.objects.all()[:3]
    return render(request, "favorites/favorites.html", {"favorites": items})