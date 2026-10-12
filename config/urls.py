from django.contrib import admin
from django.urls import path, include
from apps.core import views

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
    path("contact/", include("apps.contact.urls")),
    path("about/", views.about, name="about"),
] 