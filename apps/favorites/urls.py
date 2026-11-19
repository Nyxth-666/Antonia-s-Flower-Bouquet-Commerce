from django.urls import path
from . import views

app_name = "favorites"

urlpatterns = [
    path("", views.favorites_page, name="favorites"),
    path("toggle/<int:bouquet_id>/", views.toggle_favorite, name="toggle"),
]