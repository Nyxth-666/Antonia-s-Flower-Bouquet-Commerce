from django.shortcuts import render
from django.http import HttpRequest


def customization_page(request):
    return render(request, "customization/customization.html")