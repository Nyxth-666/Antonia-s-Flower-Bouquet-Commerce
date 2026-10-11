from django.urls import path
from . import views

app_name = "customization"

urlpatterns = [
    path("", views.customization_page, name="customization"),
]