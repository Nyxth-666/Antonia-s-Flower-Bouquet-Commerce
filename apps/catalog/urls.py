from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.catalog_page, name="catalog"),
    path("flowers-catalog/", views.flower_types_page, name="flowers-catalog"),
    path("arrangements-catalog/", views.arrangement_types_page, name="arrangements-catalog"),
]