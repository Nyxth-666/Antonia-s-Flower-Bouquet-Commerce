from django.urls import path
from . import views

urlpatterns = [
    path("", views.favorites, name="favorites"),
]

app_name = "favorites"

urlpatterns = [
    path("", views.favorites, name="favorites"),
]