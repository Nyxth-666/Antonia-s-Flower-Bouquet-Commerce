from django.conf import settings
from django.db import models


class ContactMessage(models.Model):
    class SenderType(models.TextChoices):
        USER = "USER", "User"
        GUEST = "GUEST", "Guest"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="contact_messages",
    )
    sender_type = models.CharField(
        max_length=5, choices=SenderType.choices, default=SenderType.GUEST
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"[{self.sender_type}] {self.full_name} - {self.email}"