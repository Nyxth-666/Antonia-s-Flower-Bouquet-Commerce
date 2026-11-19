import time

from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render

from apps.accounts.models import CustomerProfile
from apps.accounts.passwords import password_error_messages
from apps.catalog.models import Bouquet, Occasion
from apps.core.data.flower_meaning import FLOWER_MEANINGS
from apps.core.forms import NotificationForm, ProfileForm, StoreSettingsForm
from apps.core.models import NotificationPreference, StoreSettings


def admin_ctx(request, title, **extra):
    return {**admin.site.each_context(request), "title": title, **extra}


def first_errors(form):
    return {field: errors[0] for field, errors in form.errors.items()}


def home(request):
    return render(request, "home/home.html", {
        "occasions": Occasion.objects.filter(is_active=True),
        "flower": FLOWER_MEANINGS[int(time.time() // 1800) % len(FLOWER_MEANINGS)],
        "best_sellers": Bouquet.objects.filter(available=True).order_by("-rating")[:8],
    })


# admin page
@staff_member_required
def profile(request):
    user = request.user
    prof, _ = CustomerProfile.objects.get_or_create(user=user)
    account = {"full_name": user.get_full_name().strip() or user.username, "email": user.email, "phone": prof.phone}
    submitted = request.method == "POST" and "full_name" in request.POST
    form = ProfileForm(request.POST if submitted else None, initial=account, user=user)

    if submitted and form.is_valid():
        data = form.cleaned_data
        user.first_name, _, user.last_name = data["full_name"].partition(" ")
        user.email, prof.phone = data["email"], data["phone"]
        user.save()
        prof.save()
        messages.success(request, "Your profile was updated.")
        return redirect("admin_profile")

    return render(request, "admin/admin-profile.html", admin_ctx(
        request, "My Profile",
        profile_account=account,
        profile_values=form.data if form.is_bound else account,
        profile_errors=first_errors(form),
        profile_editing=form.is_bound,
        admin_role="Super Administrator" if user.is_superuser else "Administrator",
        joined_on=user.date_joined,
    ))


@staff_member_required
def profile_settings(request):
    store = StoreSettings.load()
    prefs, _ = NotificationPreference.objects.get_or_create(user=request.user)
    form, notify_form, password_errors = StoreSettingsForm(instance=store), NotificationForm(instance=prefs), {}

    if request.method == "POST" and "shop_name" in request.POST:
        form = StoreSettingsForm(request.POST, instance=store)
        notify_form = NotificationForm(request.POST, instance=prefs)
        if form.is_valid() and notify_form.is_valid():
            form.save()
            notify_form.save()
            messages.success(request, "Your settings were updated.")
            return redirect("admin_settings")

    elif request.method == "POST" and "old_password" in request.POST:
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            update_session_auth_hash(request, password_form.save())
            messages.success(request, "Your password was updated.")
            return redirect("admin_settings")
        password_errors = password_error_messages(password_form)

    return render(request, "admin/admin-settings.html", admin_ctx(
        request, "Settings",
        form=form,
        notify_form=notify_form,
        status_open=form["status"].value() == "open",
        status_closed=form["status"].value() == "closed",
        password_errors=password_errors,
    ))


@staff_member_required
def product(request):
    return render(request, "admin/admin-products.html", admin_ctx(request, "Products"))
