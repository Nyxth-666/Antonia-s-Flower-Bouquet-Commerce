from django.contrib import messages
from django.shortcuts import redirect, render

from .data.contact_info import CONTACT_INFO
from .forms import ContactForm
from .models import ContactMessage


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save(commit=False)

            if request.user.is_authenticated:
                contact_msg.user = request.user
                contact_msg.sender_type = ContactMessage.SenderType.USER
            else:
                contact_msg.sender_type = ContactMessage.SenderType.GUEST

            contact_msg.save()
            messages.success(request, "Salamat! Naipadala na ang message mo.")
            return redirect("contact:contact")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        form = ContactForm(initial=initial)

    return render(
        request,
        "contact/contact.html",  # i-adjust sa actual na template path mo
        {"form": form, "contact_info": CONTACT_INFO},
    )