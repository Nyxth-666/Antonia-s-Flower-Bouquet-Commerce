from django.urls import path
from . import views

app_name = "types_of_flowers"

urlpatterns = [
    path("", views.types_of_flowers, name="types_of_flowers"),
]