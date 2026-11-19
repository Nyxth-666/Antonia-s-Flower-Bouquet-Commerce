from datetime import datetime

from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from apps.accounts.models import CustomerProfile
from apps.catalog.models import Occasion, Bouquet
from apps.core.data.flower_meaning import FLOWER_MEANINGS


def home(request):
    now = datetime.now().astimezone()

    interval = int(now.timestamp() // 1800)

    index = interval % len(FLOWER_MEANINGS)
    featured_flower = FLOWER_MEANINGS[index]

    best_sellers = Bouquet.objects.filter(available=True).order_by("-rating")[:8]

    occasions = Occasion.objects.filter(is_active=True)

    return render(request, "home/home.html", {
        "occasions": occasions,
        "flower": featured_flower,
         "best_sellers": best_sellers,
    })

# admin page
@staff_member_required
def profile(request):
    user_profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    account = {"full_name": request.user.get_full_name().strip() or request.user.username, "email": request.user.email, "phone": user_profile.phone}
    values, errors = account.copy(), {}

    if request.method == "POST" and "full_name" in request.POST:
        values = {"full_name": request.POST.get("full_name", "").strip(), "email": request.POST.get("email", "").strip().lower(), "phone": request.POST.get("phone", "").strip()}
        email, phone = values["email"], values["phone"]

        if not email:
            errors["email"] = "Email is required."
        elif User.objects.filter(email__iexact=email).exclude(pk=request.user.pk).exists():
            errors["email"] = "That email is already used by another account."
        elif phone and not phone.replace("+", "").replace(" ", "").replace("-", "").isdigit():
            errors["phone"] = "Enter a valid phone number."
        else:
            request.user.first_name, _, request.user.last_name = values["full_name"].partition(" ")
            request.user.email, user_profile.phone = email, phone
            request.user.save()
            user_profile.save()
            messages.success(request, "Your profile was updated.")
            return redirect("admin_profile")

    return render(request, "admin/admin-profile.html", {**admin.site.each_context(request), "title": "My Profile", "profile_account": account, "profile_values": values, "profile_errors": errors, "profile_editing": bool(errors), "admin_role": "Super Administrator" if request.user.is_superuser else "Administrator", "joined_on": request.user.date_joined})

@staff_member_required
def profile_settings(request):
    return render(request, "admin/admin-settings.html", {**admin.site.each_context(request), "title": "Profile Settings"})

@staff_member_required
def product(request):
    return render(request, "admin/admin-products.html", {**admin.site.each_context(request), "title": "Products"}) 
