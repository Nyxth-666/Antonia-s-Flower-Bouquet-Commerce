import time
from decimal import Decimal

from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import CustomerProfile
from apps.accounts.passwords import password_error_messages
from apps.catalog.models import ArrangementType, Bouquet, Occasion
from apps.core.data.flower_meaning import FLOWER_MEANINGS
from apps.core.forms import NotificationForm, ProductForm, ProfileForm, StoreSettingsForm
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


LOW_STOCK_THRESHOLD = 5

STATUS_CHOICES = [("active", "Active"), ("out", "Out of Stock"), ("inactive", "Inactive")]
STOCK_CHOICES = [("in", "In Stock"), ("low", "Low Stock"), ("out", "Out of Stock")]

STOCK_FILTERS = {
    "in": Q(quantity__gt=LOW_STOCK_THRESHOLD),
    "low": Q(quantity__gte=1, quantity__lte=LOW_STOCK_THRESHOLD),
    "out": Q(quantity=0),
}
STATUS_FILTERS = {
    "active": Q(available=True, quantity__gt=0),
    "out": Q(quantity=0),
    "inactive": Q(available=False, quantity__gt=0),
}


def peso(amount):
    text = f"{Decimal(amount):,.2f}"
    return f"₱{text[:-3] if text.endswith('.00') else text}"


def product_status(bouquet):
    if not bouquet.quantity:
        return "out", "Out of Stock"
    return ("active", "Active") if bouquet.available else ("inactive", "Inactive")


def filter_products(request):
    products = Bouquet.objects.select_related("arrangement_type")
    query, category = request.GET.get("q", "").strip(), request.GET.get("category", "")

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
            | Q(arrangement_type__name__icontains=query)
        )
    if category.isdigit():
        products = products.filter(arrangement_type_id=category)
    for name, filters in (("stock", STOCK_FILTERS), ("status", STATUS_FILTERS)):
        if condition := filters.get(request.GET.get(name, "")):
            products = products.filter(condition)

    return products


def select_options(request, name, choices):
    current = request.GET.get(name, "")
    return [{"value": v, "label": label, "selected": v == current} for v, label in choices]


def get_product(pk):
    """The bouquet for a posted id; 404 for a malformed or missing one."""
    if not pk or not pk.isdigit():
        raise Http404("Product not found")
    return get_object_or_404(Bouquet, pk=pk)


@staff_member_required
def product(request):
    form, open_modal = ProductForm(), False

    if request.method == "POST":
        if request.POST.get("action") == "delete":
            target = get_product(request.POST.get("product_id"))
            name = target.name
            target.delete()
            messages.success(request, f"“{name}” was deleted.")
            return redirect("admin_product")

        pk = request.POST.get("product_id")
        editing = get_product(pk) if pk else None
        form = ProductForm(request.POST, request.FILES, instance=editing)

        if form.is_valid():
            saved = form.save()
            messages.success(request, f"“{saved.name}” was {'updated' if editing else 'added'}.")
            return redirect("admin_product")

        open_modal = True

    products = list(filter_products(request))
    for bouquet in products:
        bouquet.price_display = peso(bouquet.price)
        bouquet.status_key, bouquet.status_label = product_status(bouquet)

    categories = ArrangementType.objects.all()

    return render(request, "admin/admin-products.html", admin_ctx(
        request, "Products",
        products=products,
        product_form=form,
        open_product_modal=open_modal,
        editing_product=form.instance if form.instance.pk else None,
        arrangement_types=categories,
        search_query=request.GET.get("q", ""),
        category_options=select_options(request, "category", [(str(a.pk), a.name) for a in categories]),
        stock_options=select_options(request, "stock", STOCK_CHOICES),
        status_options=select_options(request, "status", STATUS_CHOICES),
    ))
