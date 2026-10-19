from django.db import models

class Occasion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class FlowerType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hex_code = models.CharField(
        max_length=7,
        help_text="Enter a HEX color code, e.g. #FFC0CB",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.name
    
class Bouquet(models.Model):
    ARRANGEMENT_CHOICES = [
        ("Chocolate Bouquets", "Chocolate Bouquets"),
        ("Flower Bouquets", "Flower Bouquets"),
        ("Flower in a Box", "Flower in a Box"),
        ("Flower in a Card", "Flower in a Card"),
        ("Flower in a Vase", "Flower in a Vase"),
        ("Inaugural Flowers", "Inaugural Flowers"),
        ("Petite Bouquets", "Petite Bouquets"),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    size = models.CharField(max_length=100)

    flower_type = models.ManyToManyField(
        FlowerType,
        blank=True,
        related_name="bouquets",
    )

    arrangement_type = models.CharField(
        max_length=50,
        choices=ARRANGEMENT_CHOICES,
    )

    color = models.ManyToManyField(
        Color,
        blank=True,
        related_name="bouquets",
    )

    occasions = models.ManyToManyField(
        Occasion,
        blank=True,
        related_name="bouquets",
    )

    image = models.ImageField(
        upload_to="bouquets/",
        blank=True,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
    )

    rating_count = models.PositiveIntegerField(default=0)

    quantity = models.PositiveIntegerField(default=0)

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
