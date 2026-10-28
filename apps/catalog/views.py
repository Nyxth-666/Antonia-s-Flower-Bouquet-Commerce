from django.shortcuts import render
from . filters import filter_bouquets
from . models import Bouquet, Occasion, Color, FlowerType
from apps.catalog.data.flower_type import FLOWER_TYPE
from apps.catalog.data.arrangement_type import ARRANGEMENT_TYPES

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

def flower_types_page(request):
    selected_type = request.GET.get("type", "")

    return render(request, "catalog/flowers-catalog.html", {
        "flower_types": FLOWER_TYPE,
        "selected_types": selected_type,
        }  
    )

def arrangement_types_page(request):
    selected_type = request.GET.get("type", "")

    return render(
        request, "catalog/arrangements-catalog.html", {
            "arrangement_types": ARRANGEMENT_TYPES,
            "selected_type": selected_type,
        }
    )