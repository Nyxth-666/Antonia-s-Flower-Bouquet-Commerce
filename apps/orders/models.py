from django.db import models
from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def item_count(self):
        standard_count = sum(
            item.quantity for item in self.items.all()
        )

        custom_count = sum(
            item.quantity for item in self.custom_items.all()
        )

        return standard_count + custom_count

    @property
    def subtotal(self):
        standard_total = sum(
            item.subtotal for item in self.items.all()
        )

        custom_total = sum(
            item.subtotal for item in self.custom_items.all()
        )

        return standard_total + custom_total

    def __str__(self):
        return f"Cart - {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    bouquet = models.ForeignKey(
        "catalog.Bouquet",
        on_delete=models.PROTECT,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.price * self.quantity

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "bouquet"],
                name="unique_bouquet_per_cart"
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="cart_item_quantity_at_least_one"
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="cart_item_price_non_negative"
            ),
        ]

    def __str__(self):
        return f"{self.bouquet.name} ({self.quantity})"

class CustomCartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="custom_items"
    )

    custom_bouquet = models.ForeignKey(
        "customization.CustomBouquet",
        on_delete=models.PROTECT,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.price * self.quantity

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "custom_bouquet"],
                name="unique_custom_bouquet_per_cart"
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="custom_cart_quantity_at_least_one"
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="custom_cart_price_non_negative"
            ),
        ]

    def __str__(self):
        return f"Custom Bouquet ({self.quantity})"