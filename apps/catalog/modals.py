
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
        on_delete=models.CASCADE,
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
            )
        ]

    def __str__(self):
        return f"{self.bouquet.name} ({self.quantity})"
