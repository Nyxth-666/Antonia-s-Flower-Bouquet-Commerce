from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from apps.catalog.models import ArrangementType, Bouquet
from apps.favorites.models import Favorite


class ToggleFavoriteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="favorite-user", password="test")
        arrangement = ArrangementType.objects.create(name="Bouquet")
        self.bouquet = Bouquet.objects.create(
            name="Test bouquet",
            description="A test bouquet",
            price="25.00",
            size="Small",
            arrangement_type=arrangement,
        )
        self.client.force_login(self.user)
        self.url = reverse("favorites:toggle", args=[self.bouquet.id])

    def test_ajax_request_adds_favorite_without_redirect(self):
        response = self.client.post(
            self.url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"bouquet_id": self.bouquet.id, "is_favorite": True},
        )
        self.assertTrue(
            Favorite.objects.filter(user=self.user, bouquet=self.bouquet).exists()
        )

    def test_ajax_request_removes_favorite_without_redirect(self):
        Favorite.objects.create(user=self.user, bouquet=self.bouquet)

        response = self.client.post(
            self.url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"bouquet_id": self.bouquet.id, "is_favorite": False},
        )
        self.assertFalse(
            Favorite.objects.filter(user=self.user, bouquet=self.bouquet).exists()
        )

    def test_regular_request_still_redirects(self):
        response = self.client.post(self.url, {"next": reverse("favorites:favorites")})

        self.assertRedirects(response, reverse("favorites:favorites"))
