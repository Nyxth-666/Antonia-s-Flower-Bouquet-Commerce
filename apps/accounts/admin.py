from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Admin, Customer


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False)


@admin.register(Admin)
class AdminUserAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)