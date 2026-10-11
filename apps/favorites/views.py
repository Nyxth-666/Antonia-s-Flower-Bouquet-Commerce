from django.shortcuts import render
from django.http import HttpRequest


def accounts_page(request):
    return render(request, "favorites/favorites.html")