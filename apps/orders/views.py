from django.shortcuts import render

def orders_page(request):
    return render(request, "orders/orders.html")