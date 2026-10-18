from django.db import models

class Occasion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Bouquet(models.Model):
    COLOR_CHOICES = [
        ("Blue", "Blue"),
        ("Champagne", "Champagne"),
        ("Green", "Green"),
        ("Orange", "Orange"),
        ("Pink", "Pink"),
        ("Purple", "Purple"),
        ("Red", "Red"),
        ("White", "White"),
        ("Yellow", "Yellow"),
    ]

    FLOWER_TYPE_CHOICES = [
        ("Carnation", "Carnation"),
        ("Gerberas", "Gerberas"),
        ("Lilies", "Lilies"),
        ("Lisianthus/Paper Roses", "Lisianthus/Paper Roses"),
        ("Tulips", "Tulips"),
        ("Roses", "Roses"),
        ("Sunflowers", "Sunflowers"),
        ("Mixed Flowers", "Mixed Flowers"),
    ]

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

    flower_type = models.CharField(
        max_length=50,
        choices=FLOWER_TYPE_CHOICES,
    )

    arrangement_type = models.CharField(
        max_length=50,
        choices=ARRANGEMENT_CHOICES,
    )

    color = models.CharField(
        max_length=30,
        choices=COLOR_CHOICES,
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
