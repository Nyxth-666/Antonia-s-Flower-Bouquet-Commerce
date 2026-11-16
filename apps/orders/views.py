from django.shortcuts import render

def orders(request):
    # Temporary, for frontend preview only
    if request.GET.get("empty"):
        items = []
    else:
        items = [
            {"name": "Rose", "price": 150, "quantity": 1, "image": ""},
        ]
    return render(request, "orders/orders.html", {
        "cart_items": items,
        "delivery_fee": 100,
    })