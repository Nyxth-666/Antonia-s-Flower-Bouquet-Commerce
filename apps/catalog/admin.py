from django.contrib import admin
from .models import (
    Bouquet,
    Color,
    FlowerType,
    Occasion,
    ArrangementType,
)
from django.utils.html import format_html

@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "description", "is_active",)
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(FlowerType)
class FlowerTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image", "is_active",)
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(ArrangementType)
class ArrangementTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image", "is_active",)
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code", "color_preview")
    search_fields = ("name", "hex_code")
    ordering = ("name",)

    @admin.display(description="Preview")
    def color_preview(self, obj):
        return format_html(
            '<span style="display:inline-block;'
            'width:25px;height:25px;border-radius:50%;'
            'border:1px solid #ccc;'
            'background-color:{};"></span>',
            obj.hex_code,
        )
    
@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "quantity",
        "available",
        "rating",
        "rating_count",
    )

    list_filter = (
        "available",
        "color",
        "occasions",
        "flower_type",
        "arrangement_type",
    )

    search_fields = (
        "name",
        "description",
        "occasions__name",
        "color__name",
    )

    list_editable = (
        "price",
        "quantity",
        "available",
    )

    filter_horizontal = (
        "flower_type", 
        "color", 
        "occasions"
    )

    ordering = ("name",)