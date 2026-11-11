from django.contrib import admin
from .models import (
    BouquetSize, FlowerOption, WrappingOption, AddOn,
    CustomBouquet, CustomBouquetFlower, CustomBouquetAddOn,
)

admin.site.register([BouquetSize, FlowerOption, WrappingOption, AddOn])

class FlowerInline(admin.TabularInline):
    model = CustomBouquetFlower
    extra = 0

class AddOnInline(admin.TabularInline):
    model = CustomBouquetAddOn
    extra = 0

@admin.register(CustomBouquet)
class CustomBouquetAdmin(admin.ModelAdmin):
    inlines = [FlowerInline, AddOnInline]
    search_fields = ("name", "user__email")