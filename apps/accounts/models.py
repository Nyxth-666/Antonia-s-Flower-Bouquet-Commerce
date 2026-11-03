from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, UserManager


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)

class Customer(User):
    objects = CustomerManager()

    class Meta:
        proxy = True
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"