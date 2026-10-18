from django.shortcuts import render
from apps.contact.data.contact_info import CONTACT_INFO

def contact_page(request):
    return render(request, "contact/contact.html", {
        "contact_info": CONTACT_INFO,
    })