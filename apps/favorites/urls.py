from django.urls import path
from . import views

urlpatterns = [
    path("", views.favorites, name="favorites"),
]

app_name = "favorites"

urlpatterns = [
    path("", views.favorites_page, name="favorites"),
    path("toggle/<int:bouquet_id>/", views.toggle_favorite, name="toggle"),
]