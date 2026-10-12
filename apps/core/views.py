from django.shortcuts import render
from apps.occasions.data.occasions import OCCASIONS

def home(request):
    return render(request, "home/home.html", {
        "occasions": OCCASIONS,
    })