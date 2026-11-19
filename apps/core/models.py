from datetime import time

from django.conf import settings
from django.db import models


class StoreSettings(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    shop_name = models.CharField(max_length=120, default="Antonia’s Flowers")
    email = models.EmailField(default="antoniaflowers@gmail.com")
    address = models.CharField(max_length=255, default="123 Flower Street, Lucena City, Quezon")
    contact = models.CharField(max_length=30, blank=True)
    description = models.TextField(default="Fresh flowers, handcrafted bouquets, and special arrangements for every occasion.")
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    opens = models.TimeField(default=time(9, 0))
    closes = models.TimeField(default=time(20, 0))
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    class Meta:
        verbose_name_plural = "Store settings"

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]

    def __str__(self):
        return self.shop_name


class NotificationPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preferences",
    )
    new_orders = models.BooleanField(default=True)
    low_stock = models.BooleanField(default=True)
    customer_messages = models.BooleanField(default=True)

    def __str__(self):
        return f"Notifications for {self.user.username}"
