from django.shortcuts import render
from .filters import filter_bouquets
from .models import Bouquet, Occasion, Color, FlowerType

def catalog_page(request):
    bouquets = filter_bouquets(request)

    context = {
        "bouquets": bouquets,
        "occasions": Occasion.objects.all(),
        "colors": Color.objects.all(),
        "flower_types": FlowerType.objects.all(),
        "arrangement_types": Bouquet.ARRANGEMENT_CHOICES,

        "selected_occasions": request.GET.getlist("occasion"),
        "selected_colors": request.GET.getlist("color"),
        "selected_flower_types": request.GET.getlist("flower_type"),
        "selected_product_types": request.GET.getlist("product_type"),
        "selected_price": request.GET.get("price", ""),
        "selected_availability": request.GET.get("availability", ""),
    }

    return render(
        request,
        "catalog/catalog.html",
        context,
    )