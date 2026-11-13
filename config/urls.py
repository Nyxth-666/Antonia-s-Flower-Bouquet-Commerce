from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from apps.about import views
from apps.core.views import profile, profile_settings, product
app_name = "types_of_flowers"

urlpatterns = [
    path("admin/profile/", profile, name="admin_profile"),
    path("admin/profile_settings", profile_settings, name="admin_settings"),
    path("admin/product", product, name="admin_product"),
    path("admin/welcome/", TemplateView.as_view(template_name="admin/welcome-admin.html"), name="admin_welcome"),
    path("admin/", admin.site.urls),

    path("", include("apps.core.urls")),

    path("catalog/", include("apps.catalog.urls")),
    path("occasions/", include("apps.occasions.urls")),
    path("customize/", include("apps.customization.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("orders/", include("apps.orders.urls")),
    path("favorites/", include("apps.favorites.urls")),
    path("about/", include("apps.about.urls")),
    path("contact/", include("apps.contact.urls")),
    
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)