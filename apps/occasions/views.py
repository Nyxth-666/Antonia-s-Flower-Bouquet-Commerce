from django.shortcuts import render
from apps.catalog.models import Occasion

def occasions_page(request):
    occasions = Occasion.objects.filter(is_active=True)
    
    return render(request, "occasions/occasions.html", {
        "occasions": occasions,
    })
