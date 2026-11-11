from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class BouquetSize(models.Model):
    name = models.CharField(max_length=50, unique=True)

    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["base_price", "name"]

    def __str__(self):
        return self.name

class FlowerOption(models.Model):
    flower_type = models.OneToOneField(
        "catalog.FlowerType",
        on_delete=models.PROTECT,
        related_name="customization_option",
    )

    price_per_stem = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    available = models.BooleanField(default=True)

    class Meta:
        ordering = ["flower_type__name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price_per_stem__gte=0),
                name="flower_option_price_non_negative",
            ),
        ]

    def __str__(self):
        return self.flower_type.name

class WrappingOption(models.Model):
    name = models.CharField(max_length=100, unique=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="wrapping_option_price_non_negative",
            ),
        ]

    def __str__(self):
        return self.name

class AddOn(models.Model):
    name = models.CharField(max_length=100, unique=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="addon_price_non_negative",
            ),
        ]

    def __str__(self):
        return self.name

class CustomBouquet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="custom_bouquets",
    )

    name = models.CharField(max_length=150, blank=True)

    size = models.ForeignKey(
        BouquetSize,
        on_delete=models.PROTECT,
        related_name="custom_bouquets",
    )

    wrapping = models.ForeignKey(
        WrappingOption,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="custom_bouquets",
    )

    wrapping_color = models.ForeignKey(
        "catalog.Color",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="custom_bouquets",
    )

    message = models.CharField(max_length=140, blank=True)

    # Saved price breakdown
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    flowers_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    wrapping_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    addons_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    base_price__gte=0,
                    flowers_total__gte=0,
                    wrapping_total__gte=0,
                    addons_total__gte=0,
                    total_price__gte=0,
                ),
                name="custom_bouquet_prices_non_negative",
            ),
        ]

    def __str__(self):
        return self.name or f"Custom bouquet #{self.pk}"

class CustomBouquetFlower(models.Model):
    custom_bouquet = models.ForeignKey(
        CustomBouquet,
        on_delete=models.CASCADE,
        related_name="flowers",
    )

    flower = models.ForeignKey(
        FlowerOption,
        on_delete=models.PROTECT,
        related_name="custom_bouquet_selections",
    )

    quantity = models.PositiveIntegerField(default=1)

    # Price snapshot at the time of selection
    price_per_stem = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    @property
    def subtotal(self):
        return self.price_per_stem * self.quantity

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["custom_bouquet", "flower"],
                name="unique_flower_per_custom_bouquet",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="custom_flower_quantity_at_least_one",
            ),
            models.CheckConstraint(
                condition=models.Q(price_per_stem__gte=0),
                name="custom_flower_price_non_negative",
            ),
        ]

    def __str__(self):
        return f"{self.flower} x {self.quantity}"

class CustomBouquetAddOn(models.Model):
    custom_bouquet = models.ForeignKey(
        CustomBouquet,
        on_delete=models.CASCADE,
        related_name="addons",
    )

    addon = models.ForeignKey(
        AddOn,
        on_delete=models.PROTECT,
        related_name="custom_bouquet_selections",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["custom_bouquet", "addon"],
                name="unique_addon_per_custom_bouquet",
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="custom_addon_price_non_negative",
            ),
        ]

    def __str__(self):
        return f"{self.addon.name} - {self.custom_bouquet}"