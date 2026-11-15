from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "sender_type", "is_read", "created_at")
    list_filter = ("sender_type", "is_read", "created_at")
    search_fields = ("first_name", "last_name", "email", "message")