from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import ArrangementType, Bouquet
from .models import CartItem


class CartPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="flower-shopper",
            password="test-password",
        )
        self.client.force_login(self.user)
        arrangement_type = ArrangementType.objects.create(name="Bouquet")
        self.bouquet = Bouquet.objects.create(
            name="Red Roses",
            description="A bouquet of red roses.",
            price=Decimal("150.00"),
            size="Small",
            arrangement_type=arrangement_type,
            quantity=5,
            available=True,
        )

    def test_cart_displays_bouquet_added_from_catalog(self):
        add_response = self.client.post(
            reverse("orders:add_to_cart", args=[self.bouquet.pk]),
        )

        self.assertRedirects(add_response, reverse("orders:cart"))
        response = self.client.get(reverse("orders:cart"))

        self.assertTemplateUsed(response, "cart/cart.html")
        self.assertContains(response, "Red Roses")
        self.assertContains(response, "₱150.00")
        self.assertContains(response, "₱250.00")

    def test_ajax_add_to_cart_returns_without_redirecting(self):
        response = self.client.post(
            reverse("orders:add_to_cart", args=[self.bouquet.pk]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "success": True,
                "message": "Red Roses added to cart.",
                "item_count": 1,
            },
        )
        self.assertEqual(
            CartItem.objects.get(bouquet=self.bouquet).quantity,
            1,
        )

    def test_ajax_quantity_update_returns_updated_totals(self):
        self.client.post(reverse("orders:add_to_cart", args=[self.bouquet.pk]))
        item = CartItem.objects.get(bouquet=self.bouquet)

        response = self.client.post(
            reverse("orders:update_item", args=["bouquet", item.pk]),
            {"quantity": 2},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "success": True,
                "item_count": 2,
                "subtotal": "300.00",
                "total": "400.00",
                "empty": False,
                "deleted": False,
                "quantity": 2,
                "line_total": "300.00",
            },
        )

    def test_clear_cart_removes_cart_items(self):
        self.client.post(reverse("orders:add_to_cart", args=[self.bouquet.pk]))
        item = CartItem.objects.get(bouquet=self.bouquet)

        response = self.client.post(reverse("orders:clear_cart"))

        self.assertRedirects(response, reverse("orders:cart"))
        self.assertFalse(CartItem.objects.filter(pk=item.pk).exists())
        self.assertContains(self.client.get(reverse("orders:cart")), "Your cart is empty")
