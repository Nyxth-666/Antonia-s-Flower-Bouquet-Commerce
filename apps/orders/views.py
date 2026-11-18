from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalog.models import Bouquet
from .models import Cart, CartItem, CustomCartItem


def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
@require_POST
def add_to_cart(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    quantity = max(int(request.POST.get("quantity", 1)), 1)
    cart = _get_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        bouquet=bouquet,
        defaults={"price": bouquet.price, "quantity": quantity},
    )
    if not created:
        item.quantity += quantity
        item.save()

    messages.success(request, f"{bouquet.name} added to cart.")
    return redirect(request.POST.get("next") or "orders:cart")


@login_required
def cart_page(request):
    cart = _get_cart(request.user)
    context = {
        "cart": cart,
        "items": cart.items.select_related("bouquet"),
        "custom_items": cart.custom_items.select_related("custom_bouquet"),
    }
    return render(request, "orders/cart.html", context)


def _get_item(request, kind, item_id):
    model = CustomCartItem if kind == "custom" else CartItem
    return get_object_or_404(model, pk=item_id, cart__user=request.user)


@login_required
@require_POST
def update_item(request, kind, item_id):
    item = _get_item(request, kind, item_id)
    quantity = int(request.POST.get("quantity", 1))
    if quantity < 1:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    return redirect("orders:cart")


@login_required
@require_POST
def remove_item(request, kind, item_id):
    _get_item(request, kind, item_id).delete()
    return redirect("orders:cart")

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