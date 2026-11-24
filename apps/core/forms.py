from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from apps.catalog.models import Bouquet
from apps.core.models import NotificationPreference, StoreSettings

phone_validator = RegexValidator(r"^\+?[\d\s-]+$", "Enter a valid phone number.")


class ProfileForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    phone = forms.CharField(required=False, validators=[phone_validator])

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("That email is already used by another account.")
        return email


class StoreSettingsForm(forms.ModelForm):
    delivery_fee = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)
    minimum_order = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)

    class Meta:
        model = StoreSettings
        fields = ["shop_name", "email", "address", "contact", "description", "delivery_fee", "minimum_order", "opens", "closes", "status"]
        widgets = {field: forms.TimeInput(format="%H:%M", attrs={"type": "time"}) for field in ("opens", "closes")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ("opens", "closes"):
            value = self.initial.get(field)
            if hasattr(value, "strftime"):
                self.initial[field] = value.strftime("%H:%M")

    def clean_contact(self):
        contact = self.cleaned_data["contact"]
        if contact:
            phone_validator(contact)
        return contact

    def clean(self):
        data = super().clean()
        if data.get("opens") and data.get("closes") and data["closes"] <= data["opens"]:
            self.add_error("closes", "Closing time must be after opening time.")
        return data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Bouquet
        fields = ["name", "description", "price", "size", "arrangement_type", "quantity", "available", "image"]

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price


class NotificationForm(forms.ModelForm):
    class Meta:
        model = NotificationPreference
        fields = ["new_orders", "low_stock", "customer_messages"]
