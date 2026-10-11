from django.urls import path
from . import views

app_name = "occasions"

urlpatterns = [
    path("", views.occasions_page, name="occasions"),
]