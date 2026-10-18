from django.contrib import admin
from django.urls import path, include

from apps.about import views
app_name = "types_of_flowers"
urlpatterns = [
    path("admin/", admin.site.urls),

    # Homepage
    path("", include("apps.core.urls")),

    # Website features
    path("catalog/", include("apps.catalog.urls")),
    path("occasions/", include("apps.occasions.urls")),
    path("customize/", include("apps.customization.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("orders/", include("apps.orders.urls")),
    path("favorites/", include("apps.favorites.urls")),
    path("about/", include("apps.about.urls")),
    path("contact/", include("apps.contact.urls")),
    path("types-of-flowers/", include("apps.types_of_flowers.urls")),
]