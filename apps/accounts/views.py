from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomerProfile

from .forms import RegisterForm

PROFILE_TABS = [
    {"page": "profile",  "label": "Profile",   "template": "components/ui/cards/change-profile-card.html"},
    {"page": "orders",   "label": "My Orders", "template": "components/ui/cards/my-orders-card.html"},
    {"page": "settings", "label": "Settings",  "template": "components/ui/cards/profile-settings-card.html"},
]

SAMPLE_ORDER = [
    {"order_id": "PS-48213", "order_date": "Sep 12, 2026", "status": "Delivered",
     "item": "Medium Custom Bouquet", "price": "₱1180", "item_count": "1 item"},
    {"order_id": "PS-48214", "order_date": "Sep 12, 2026", "status": "Out for delivery",
     "item": "Medium Custom Bouquet", "price": "₱1180", "item_count": "1 item"},
    {"order_id": "PS-48215", "order_date": "Sep 12, 2026", "status": "Confirmed",
     "item": "Medium Custom Bouquet", "price": "₱1180", "item_count": "1 item"},
    {"order_id": "PS-48215", "order_date": "Sep 12, 2026", "status": "Preparing",
    "item": "Medium Custom Bouquet", "price": "₱1180", "item_count": "1 item"},
]
STATUS_STEPS = {"Confirmed": 0, "Preparing": 1, "Out for delivery": 2, "Delivered": 3}
ORDER_STEPS = list(STATUS_STEPS)

PASSWORD_MESSAGES = {
    "password_too_common": "This password is too weak. Try something longer and less predictable.",
    "password_entirely_numeric": "This password is too weak. Add some letters.",
    "password_too_short": "This password is too weak. Use at least 8 characters.",
    "password_too_similar": "This password is too similar to your personal details.",
}


def password_error_messages(form):
    errors = {}
    for field, error_list in form.errors.as_data().items():
        for err in error_list:
            if err.code in PASSWORD_MESSAGES:
                errors.setdefault("new_password1", PASSWORD_MESSAGES[err.code])
            else:
                errors.setdefault(field, err.messages[0])
    return errors

@login_required
def accounts_page(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)

    errors = {}
    values = {
        "full_name": request.user.get_full_name(),
        "email": request.user.email,
        "phone": profile.phone,
    }

    if request.method == "POST" and "full_name" in request.POST:
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()
        values = {"full_name": full_name, "email": email, "phone": phone}

        if not email:
            errors["email"] = "Email is required."
        elif User.objects.filter(email__iexact=email).exclude(pk=request.user.pk).exists():
            errors["email"] = "That email is already used by another account."
        elif phone and not phone.replace("+", "").replace(" ", "").replace("-", "").isdigit():
            errors["phone"] = "Enter a valid phone number."
        else:
            first_name, _, last_name = full_name.partition(" ")
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            profile.phone = phone
            profile.save()
            messages.success(request, "Your profile was updated.")
            return redirect("accounts:accounts")

    orders = [{**o, "step": STATUS_STEPS.get(o["status"], -1)} for o in SAMPLE_ORDER]

    password_form = PasswordChangeForm(request.user)
    password_errors = {}

    if request.method == "POST" and "old_password" in request.POST:
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was updated.")
            return redirect("accounts:accounts")
        password_errors = password_error_messages(password_form)
        
    return render(request, "accounts/accounts.html", {
        "profile_tabs": PROFILE_TABS,
        "sample_order": orders,
        "steps": ORDER_STEPS,
        "profile_errors": errors,
        "password_form": password_form,
        "profile_values": values,
        "password_errors": password_errors,
    })

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:accounts")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomerProfile.objects.create(user=user)
            login(request, user)
            return redirect("accounts:accounts")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})