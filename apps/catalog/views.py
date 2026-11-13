from django.shortcuts import render
from . filters import filter_bouquets
from . models import (
    Bouquet,
    Occasion,
    Color,
    FlowerType,
    ArrangementType,
)

def catalog_page(request):
    bouquets = filter_bouquets(request)

    context = {
        "bouquets": bouquets,

        "occasions": Occasion.objects.filter(is_active=True),
        "colors": Color.objects.all(),
        "flower_types": FlowerType.objects.filter(is_active=True),
        "arrangement_types": ArrangementType.objects.filter(is_active=True),

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

    context = {
        "flower_types": FlowerType.objects.filter(is_active=True),
        "selected_type": selected_type,
    }

    return render(
        request,
        "catalog/flowers-catalog.html",
        context,
    )

def arrangement_types_page(request):
    selected_type = request.GET.get("type", "")

    context = {
        "arrangement_types": ArrangementType.objects.filter(is_active=True),
        "selected_type": selected_type,
    }

    return render(
        request,
        "catalog/arrangements-catalog.html",
        context,
    )