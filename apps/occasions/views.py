from django.shortcuts import render
from django.http import HttpRequest


def occasions_page(request):
    return render(request, "occasions/occasions.html")