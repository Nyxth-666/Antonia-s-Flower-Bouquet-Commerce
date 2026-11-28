from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalog.models import Bouquet
from .models import Cart, CartItem, CustomCartItem

DELIVERY_FEE = Decimal("100.00")


def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def _cart_update_response(cart, item=None):
    item_count = cart.item_count
    subtotal = cart.subtotal
    return JsonResponse({
        "success": True,
        "item_count": item_count,
        "subtotal": str(subtotal),
        "total": str(subtotal + DELIVERY_FEE),
        "empty": item_count == 0,
        "deleted": item is None,
        "quantity": item.quantity if item is not None else None,
        "line_total": str(item.subtotal) if item is not None else "0.00",
    })


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

    message = f"{bouquet.name} added to cart."
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "message": message,
            "item_count": cart.item_count,
        })

    messages.success(request, message)
    return redirect(request.POST.get("next") or "orders:cart")


@login_required
def cart_page(request):
    cart = _get_cart(request.user)
    delivery_fee = DELIVERY_FEE
    subtotal = cart.subtotal
    context = {
        "cart": cart,
        "items": cart.items.select_related("bouquet"),
        "custom_items": cart.custom_items.select_related("custom_bouquet"),
        "item_count": cart.item_count,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": subtotal + delivery_fee,
    }
    return render(request, "cart/cart.html", context)


def _get_item(request, kind, item_id):
    model = CustomCartItem if kind == "custom" else CartItem
    return get_object_or_404(model, pk=item_id, cart__user=request.user)


@login_required
@require_POST
def update_item(request, kind, item_id):
    item = _get_item(request, kind, item_id)
    cart = item.cart
    quantity = int(request.POST.get("quantity", 1))
    if quantity < 1:
        item.delete()
        item = None
    else:
        item.quantity = quantity
        item.save()
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return _cart_update_response(cart, item)
    return redirect("orders:cart")


@login_required
@require_POST
def remove_item(request, kind, item_id):
    item = _get_item(request, kind, item_id)
    cart = item.cart
    item.delete()
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return _cart_update_response(cart)
    return redirect("orders:cart")


@login_required
@require_POST
def clear_cart(request):
    cart = _get_cart(request.user)
    cart.items.all().delete()
    cart.custom_items.all().delete()
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return _cart_update_response(cart)
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