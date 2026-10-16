from django.shortcuts import render
from apps.occasions.data.occasions import OCCASIONS

def occasions_page(request):
    context = {
        "occasions": OCCASIONS,
    }
    
    return render(request, "occasions/occasions.html", context)
