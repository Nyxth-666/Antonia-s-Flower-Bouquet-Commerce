from django.shortcuts import render
from django.http import HttpRequest


def favorites_page(request):
    return render(request, "favorites/favorites.html")