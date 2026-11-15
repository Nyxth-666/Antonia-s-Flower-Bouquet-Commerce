from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    accepted_terms = forms.BooleanField(
        required=True,
        error_messages={"required": "Please accept the terms of agreement."},
    )

    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "email", "phone", "message"]