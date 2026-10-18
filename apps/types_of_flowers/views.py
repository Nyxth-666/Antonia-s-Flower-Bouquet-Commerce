from django.shortcuts import render

def types_of_flowers(request):
    flowertypes = [
        {"name": "Lisianthus/Paper Roses"},
        {"name": "Tulips"},
        {"name": "Lilies"},
        {"name": "Carnation"},
        {"name": "Sunflowers"},
        {"name": "Gerberas"},
        {"name": "Roses"},
        {"name": "Mixed Flowers"},
    ]
    return render(request, "types-of-flowers/types-of-flowers.html", {"flowertypes": flowertypes})