from django.shortcuts import render
from . models import Bouquet


def catalog_page(request):
    bouquets = Bouquet.objects.all()

    return render(
        request,
        "catalog/catalog.html",
        {"bouquets": bouquets},
    )