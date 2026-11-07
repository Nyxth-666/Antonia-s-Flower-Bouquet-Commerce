from django.conf import settings
from django.db import models



class BouquetSize(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Small, Medium, Large, Extra Large
    base_price = models.DecimalField(max_digits=10, decimal_places=2)  # Large = 800

    def __str__(self):
        return self.name


class FlowerOption(models.Model):
    flower_type = models.OneToOneField("catalog.FlowerType", on_delete=models.CASCADE)
    price_per_stem = models.DecimalField(max_digits=10, decimal_places=2)  # ₱55 / stem
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.flower_type.name


class WrappingOption(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Kraft paper, White paper, Satin wrap, Luxury box
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class AddOn(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Chocolate box, Teddy bear, Greeting card, Balloon
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 180, 220, 40, 90

    def __str__(self):
        return self.name



class CustomBouquet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="custom_bouquets",
    )
    name = models.CharField(max_length=150, blank=True)  # "Name this design (optional)"
    size = models.ForeignKey(BouquetSize, on_delete=models.PROTECT)
    wrapping = models.ForeignKey(WrappingOption, on_delete=models.PROTECT, null=True, blank=True)
    wrapping_color = models.ForeignKey("catalog.Color", on_delete=models.PROTECT, null=True, blank=True)
    message = models.CharField(max_length=140, blank=True)  # 0/140 sa page

    # price breakdown (sine-save para hindi magbago kapag nag-iba ang presyo later)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    flowers_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wrapping_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    addons_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name or f"Custom bouquet #{self.pk}"


class CustomBouquetFlower(models.Model):
    custom_bouquet = models.ForeignKey(CustomBouquet, on_delete=models.CASCADE, related_name="flowers")
    flower = models.ForeignKey(FlowerOption, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_per_stem = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["custom_bouquet", "flower"], name="unique_flower_per_custom_bouquet")
        ]


class CustomBouquetAddOn(models.Model):
    custom_bouquet = models.ForeignKey(CustomBouquet, on_delete=models.CASCADE, related_name="addons")
    addon = models.ForeignKey(AddOn, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["custom_bouquet", "addon"], name="unique_addon_per_custom_bouquet")
        ]