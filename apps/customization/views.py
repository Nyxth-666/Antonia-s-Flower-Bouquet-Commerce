from django.shortcuts import render
from apps.catalog.models import Color
from .models import (
    BouquetSize,
    FlowerOption,
    WrappingOption,
    AddOn,
)

def customization_page(request):
    sizes = BouquetSize.objects.filter(is_active=True)

    flowers = FlowerOption.objects.filter(
        available=True,
        flower_type__is_active=True,
    ).select_related("flower_type")

    colors = Color.objects.all()

    wrapping_options = WrappingOption.objects.filter(
        is_active=True
    )

    addons = AddOn.objects.filter(
        is_active=True
    )

    context = {
        "sizes": sizes,
        "flowers": flowers,
        "colors": colors,
        "wrapping_options": wrapping_options,
        "addons": addons,
    }

    return render(
        request,
        "customization/customization.html",
        context,
    )