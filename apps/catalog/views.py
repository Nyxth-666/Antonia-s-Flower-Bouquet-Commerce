from django.shortcuts import render
from django.http import HttpRequest


def catalog_page(request):
    return render(request, "catalog/catalog.html")