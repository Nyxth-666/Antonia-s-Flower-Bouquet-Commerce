from django.shortcuts import render
from apps.occasions.data.occasions import OCCASIONS

BEST_SELLERS = [
    {
        "name": "Red Rose",
        "price": "₱55/stem",
        "description": "Love and passion — the classic romantic gesture.",
        "image": "red-rose.svg",
        "colors": ["#D14C52", "#E8A2B1", "#E7DCC8"],
    },
    {
        "name": "Pink Lily",
        "price": "₱48/stem",
        "description": "Grace and affection to brighten any thoughtful gift.",
        "image": "pink-lily.svg",
        "colors": ["#D87994", "#F2C6D8", "#EAE2D3"],
    },
    {
        "name": "White Orchid",
        "price": "₱62/stem",
        "description": "Purity and elegance for celebrations and quiet moments.",
        "image": "white-orchid.svg",
        "colors": ["#D8D1C9", "#F1F1F1", "#D3C6B6"],
    },
    {
        "name": "Yellow Daisy",
        "price": "₱42/stem",
        "description": "Joy and optimism for cheerful surprises and sunshine.",
        "image": "yellow-daisy.svg",
        "colors": ["#F4C24C", "#F8E795", "#D4C2A3"],
    },
    {
        "name": "Peach Carnation",
        "price": "₱38/stem",
        "description": "Warm gratitude and appreciation for special people.",
        "image": "peach-carnation.svg",
        "colors": ["#E79A62", "#F8D9A0", "#F9F1DF"],
    },
    {
        "name": "Lavender Bouquet",
        "price": "₱58/stem",
        "description": "Calm and serenity for heartfelt messages of love.",
        "image": "lavender-bouquet.svg",
        "colors": ["#A28AC5", "#D7C2EA", "#EFE7F8"],
    },
]


def home(request):
    return render(request, "home/home.html", {
        "occasions": OCCASIONS,
        "best_sellers": BEST_SELLERS,
    })