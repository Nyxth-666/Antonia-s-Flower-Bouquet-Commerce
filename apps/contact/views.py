from django.shortcuts import render
from django.http import HttpRequest


def contact_page(request):
    return render(request, "contact/contact.html")