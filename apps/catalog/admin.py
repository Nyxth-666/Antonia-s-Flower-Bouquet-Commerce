from django.contrib import admin
from .models import Bouquet, Occasion

@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "flower_type",
        "color",
        "available",
        "rating",
        "rating_count",
    )

    list_filter = (
        "available",
        "color",
        "flower_type",
        "arrangement_type",
    )

    search_fields = (
        "name",
        "description",
        "occasion",
    )

    list_editable = (
        "price",
        "available",
    )

    ordering = ("name",)
