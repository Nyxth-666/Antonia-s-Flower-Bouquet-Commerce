from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_page, name="cart"),
    path("cart/add/<int:bouquet_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<str:kind>/<int:item_id>/", views.update_item, name="update_item"),
    path("cart/remove/<str:kind>/<int:item_id>/", views.remove_item, name="remove_item"),
]