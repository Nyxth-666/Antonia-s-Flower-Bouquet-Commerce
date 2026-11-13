
from django.contrib import admin
from .models import Cart, CartItem, CustomCartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ("bouquet", "quantity", "price", "subtotal")
    readonly_fields = ("subtotal",)
    autocomplete_fields = ("bouquet",)


class CustomCartItemInline(admin.TabularInline):
    model = CustomCartItem
    extra = 0
    fields = ("custom_bouquet", "quantity", "price", "subtotal")
    readonly_fields = ("subtotal",)
    autocomplete_fields = ("custom_bouquet",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "item_count",
        "subtotal",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    list_filter = ("created_at", "updated_at")

    readonly_fields = (
        "created_at",
        "updated_at",
        "item_count",
        "subtotal",
    )

    inlines = [
        CartItemInline,
        CustomCartItemInline,
    ]

    ordering = ("-updated_at",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "bouquet",
        "quantity",
        "price",
        "subtotal",
    )

    search_fields = (
        "bouquet__name",
        "cart__user__email",
    )

    list_filter = ("cart__created_at",)

    readonly_fields = ("subtotal",)

    autocomplete_fields = ("cart", "bouquet")


@admin.register(CustomCartItem)
class CustomCartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "custom_bouquet",
        "quantity",
        "price",
        "subtotal",
    )

    search_fields = (
        "custom_bouquet__name",
        "cart__user__email",
    )

    list_filter = ("cart__created_at",)

    readonly_fields = ("subtotal",)

    autocomplete_fields = ("cart", "custom_bouquet")
