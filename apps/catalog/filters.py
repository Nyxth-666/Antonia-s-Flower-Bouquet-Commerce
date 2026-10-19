from django.db.models import Q
from .models import Bouquet, Occasion, Color, FlowerType

def filter_bouquets(request):
    bouquets = Bouquet.objects.all()

    occasion_ids = request.GET.getlist("occasion")
    if occasion_ids:
        bouquets = bouquets.filter(
            occasions__id__in=occasion_ids
        )

    color_ids = request.GET.getlist("color")
    if color_ids:
        bouquets = bouquets.filter(
            color__id__in=color_ids
        )

    flower_type_ids = request.GET.getlist("flower_type")
    if flower_type_ids:
        bouquets = bouquets.filter(
            flower_type__id__in=flower_type_ids
        )

    arrangement_types = request.GET.getlist("product_type")
    if arrangement_types:
        bouquets = bouquets.filter(
            arrangement_type__in=arrangement_types
        )

    price_range = request.GET.get("price")

    if price_range == "budget":
        bouquets = bouquets.filter(price__lt=1000)

    elif price_range == "mid":
        bouquets = bouquets.filter(
            price__gte=1000,
            price__lt=3000,
        )

    elif price_range == "premium":
        bouquets = bouquets.filter(price__gte=3000)

    availability = request.GET.get("availability")

    if availability == "available":
        bouquets = bouquets.filter(
            available=True,
            quantity__gt=0,
        )

    elif availability == "unavailable":
        bouquets = bouquets.filter(
            Q(available=False) | Q(quantity=0)
        )

    return bouquets.distinct()