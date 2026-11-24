import time
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import (
    Count,
    DecimalField,
    Exists,
    ExpressionWrapper,
    F,
    OuterRef,
    Q,
    Sum,
)
from django.db.models.functions import TruncMonth, TruncYear
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.models import Customer, CustomerProfile
from apps.accounts.passwords import password_error_messages
from apps.catalog.models import ArrangementType, Bouquet, Occasion
from apps.contact.models import ContactMessage
from apps.core.data.flower_meaning import FLOWER_MEANINGS
from apps.core.forms import NotificationForm, ProductForm, ProfileForm, StoreSettingsForm
from apps.core.models import NotificationPreference, StoreSettings
from apps.customization.models import CustomBouquet
from apps.favorites.models import Favorite
from apps.orders.models import Cart, CartItem, CustomCartItem


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


# ---------------------------------------------------------------------------
# Admin dashboard
# ---------------------------------------------------------------------------

PERIOD_CHOICES = [
    ("7", "Last 7 days"),
    ("30", "Last 30 days"),
    ("90", "Last 90 days"),
    ("365", "Last 12 months"),
]
PERIOD_DAYS = {value: int(value) for value, _ in PERIOD_CHOICES}
PERIOD_LABELS = dict(PERIOD_CHOICES)

# Shared by inventory and cart value aggregations (both use price * quantity).
LINE_TOTAL = ExpressionWrapper(
    F("price") * F("quantity"),
    output_field=DecimalField(max_digits=14, decimal_places=2),
)


def pct_trend(current, previous, up_is_good=True):
    current = Decimal(current or 0)
    previous = Decimal(previous or 0)

    if previous == 0:
        if current == 0:
            return {"label": "No change", "tone": "neutral", "arrow": False}
        return {
            "label": "New",
            "tone": "positive" if up_is_good else "warning",
            "arrow": False,
        }

    change = (current - previous) / previous * 100
    tone = "positive" if change > 0 else "negative" if change < 0 else "neutral"
    if not up_is_good and change > 0:
        tone = "warning"
    return {"label": f"{change:+.1f}%", "tone": tone, "arrow": change != 0}


def compact_number(value):
    value = float(value or 0)
    if value >= 1_000_000:
        text, suffix = f"{value / 1_000_000:.1f}", "M"
    elif value >= 1_000:
        text, suffix = f"{value / 1_000:.1f}", "k"
    else:
        return f"{value:,.0f}"
    return text.rstrip("0").rstrip(".") + suffix


def peso_compact(amount):
    return f"₱{compact_number(amount)}"


def add_months(date, months):
    month_index = date.month - 1 + months
    year = date.year + month_index // 12
    month = month_index % 12 + 1
    return date.replace(year=year, month=month, day=1)


def last_month_starts(count=6):
    first = timezone.localdate().replace(day=1)
    return [add_months(first, -offset) for offset in range(count - 1, -1, -1)]


def last_years(count=5):
    current = timezone.localdate().year
    return list(range(current - count + 1, current + 1))


def monthly_activity(months=6):
    starts = last_month_starts(months)
    # Filter on the datetime column directly (not created_at__date) so the
    # predicate stays sargable and can use an index if one is added.
    window_start = timezone.make_aware(datetime.combine(starts[0], time.min))
    rows = (
        CustomBouquet.objects.filter(created_at__gte=window_start)
        .annotate(bucket=TruncMonth("created_at"))
        .values("bucket")
        .annotate(value=Sum("total_price"), count=Count("id"))
        .order_by("bucket")
    )
    data = {(row["bucket"].year, row["bucket"].month): row for row in rows}

    items = []
    for start in starts:
        row = data.get((start.year, start.month), {})
        items.append({
            "label": start.strftime("%b"),
            "value": row.get("value") or Decimal("0"),
            "count": row.get("count") or 0,
        })
    return items


def yearly_activity(years=5):
    year_list = last_years(years)
    window_start = timezone.make_aware(datetime(year_list[0], 1, 1))
    rows = (
        CustomBouquet.objects.filter(created_at__gte=window_start)
        .annotate(bucket=TruncYear("created_at"))
        .values("bucket")
        .annotate(value=Sum("total_price"), count=Count("id"))
        .order_by("bucket")
    )
    data = {row["bucket"].year: row for row in rows}

    items = []
    for year in year_list:
        row = data.get(year, {})
        items.append({
            "label": str(year),
            "value": row.get("value") or Decimal("0"),
            "count": row.get("count") or 0,
        })
    return items


def build_bar_chart(items):
    values = [item["value"] for item in items]
    max_value = max(values) if values else Decimal("0")
    has_data = max_value > 0

    for item in items:
        item["display"] = peso(item["value"])
        item["title"] = f'{item["label"]}: {item["display"]}'
        item["current"] = item is items[-1]
        if has_data and item["value"] > 0:
            item["height"] = max(round(float(item["value"] / max_value * 100), 1), 3)
        else:
            item["height"] = 0

    if has_data:
        ticks = [
            {
                "label": peso_compact(max_value * Decimal(str(fraction))),
                "top": round((1 - fraction) * 100, 1),
            }
            for fraction in (1, 2 / 3, 1 / 3, 0)
        ]
    else:
        ticks = [
            {"label": "₱0", "top": 0},
            {"label": "₱0", "top": 33.3},
            {"label": "₱0", "top": 66.7},
            {"label": "₱0", "top": 100},
        ]

    total = sum(values, Decimal("0"))
    return {
        "items": items,
        "has_data": has_data,
        "ticks": ticks,
        "total": total,
        "total_display": peso(total),
        "count": sum(item["count"] for item in items),
    }


def build_area_chart(items, width=320, height=96, padding=4):
    cumulative = []
    total = Decimal("0")
    for item in items:
        total += item["value"]
        cumulative.append(total)

    max_value = max(cumulative) if cumulative else Decimal("0")
    step = (width - 2 * padding) / max(len(cumulative) - 1, 1)
    points = []
    for index, value in enumerate(cumulative):
        ratio = float(value / max_value) if max_value else 0
        points.append((
            padding + index * step,
            height - padding - ratio * (height - 2 * padding),
        ))

    line = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    area = line + (
        f" L {points[-1][0]:.1f},{height - padding}"
        f" L {points[0][0]:.1f},{height - padding} Z"
    )
    return {
        "line": line,
        "area": area,
        "last_x": round(points[-1][0], 1),
        "last_y": round(points[-1][1], 1),
        "labels": [item["label"] for item in items],
        "has_data": max_value > 0,
    }


@staff_member_required
def dashboard(request):
    period_key = request.GET.get("period", "30")
    if period_key not in PERIOD_DAYS:
        period_key = "30"

    period_days = PERIOD_DAYS[period_key]
    period_label = PERIOD_LABELS[period_key]
    period_choices = [
        {"value": value, "label": label, "selected": value == period_key}
        for value, label in PERIOD_CHOICES
    ]

    now = timezone.now()
    period_start_dt = now - timedelta(days=period_days)
    previous_start_dt = period_start_dt - timedelta(days=period_days)
    period_end = timezone.localdate()
    period_start = period_end - timedelta(days=period_days - 1)

    store = StoreSettings.load()
    admin_name = request.user.get_full_name().strip() or request.user.username

    # Inventory
    product_stats = Bouquet.objects.aggregate(
        total=Count("id"),
        active=Count("id", filter=Q(available=True, quantity__gt=0)),
        low=Count("id", filter=Q(quantity__gt=0, quantity__lte=LOW_STOCK_THRESHOLD)),
        out=Count("id", filter=Q(quantity=0)),
        units=Sum("quantity"),
        value=Sum(LINE_TOTAL),
    )
    product_count = product_stats["total"] or 0
    total_units = product_stats["units"] or 0
    inventory_value = product_stats["value"] or Decimal("0")

    low_stock_products = list(
        Bouquet.objects.filter(quantity__lte=LOW_STOCK_THRESHOLD)
        .select_related("arrangement_type")
        .order_by("quantity", "name")[:4]
    )
    for product in low_stock_products:
        if product.quantity == 0:
            product.stock_label = "Out of stock"
            product.stock_tone = "error"
        else:
            product.stock_label = f"{product.quantity} left"
            product.stock_tone = "warning"

    # Custom bouquets / studio
    custom_stats = CustomBouquet.objects.aggregate(
        total_count=Count("id"),
        total_value=Sum("total_price"),
        period_count=Count("id", filter=Q(created_at__gte=period_start_dt)),
        period_value=Sum("total_price", filter=Q(created_at__gte=period_start_dt)),
        previous_value=Sum(
            "total_price",
            filter=Q(created_at__gte=previous_start_dt, created_at__lt=period_start_dt),
        ),
    )
    custom_total_count = custom_stats["total_count"] or 0
    custom_total_value = custom_stats["total_value"] or Decimal("0")
    custom_period_count = custom_stats["period_count"] or 0
    custom_period_value = custom_stats["period_value"] or Decimal("0")
    custom_period_trend = pct_trend(
        custom_period_value,
        custom_stats["previous_value"] or Decimal("0"),
    )

    monthly_items = monthly_activity()
    monthly_chart = build_bar_chart(monthly_items)
    annual_chart = build_bar_chart(yearly_activity())
    studio_area = build_area_chart(monthly_items)

    in_cart_query = CustomCartItem.objects.filter(custom_bouquet=OuterRef("pk"))
    recent_builds = list(
        CustomBouquet.objects.select_related("user", "size")
        .annotate(in_cart=Exists(in_cart_query))
        .order_by("-created_at")[:5]
    )
    for build in recent_builds:
        customer_name = build.user.get_full_name().strip() or build.user.username
        build.customer_name = customer_name
        build.reference = f"CB-{build.pk:04d}"
        build.total_display = peso(build.total_price)
        build.status_label = "In cart" if build.in_cart else "Saved"
        build.status_tone = "success" if build.in_cart else "neutral"

    # Carts
    week_start = now - timedelta(days=7)
    previous_week_start = week_start - timedelta(days=7)
    standard_cart_stats = CartItem.objects.aggregate(
        total=Sum(LINE_TOTAL),
        week=Sum(LINE_TOTAL, filter=Q(cart__updated_at__gte=week_start)),
        previous=Sum(
            LINE_TOTAL,
            filter=Q(cart__updated_at__gte=previous_week_start, cart__updated_at__lt=week_start),
        ),
    )
    custom_cart_stats = CustomCartItem.objects.aggregate(
        total=Sum(LINE_TOTAL),
        week=Sum(LINE_TOTAL, filter=Q(cart__updated_at__gte=week_start)),
        previous=Sum(
            LINE_TOTAL,
            filter=Q(cart__updated_at__gte=previous_week_start, cart__updated_at__lt=week_start),
        ),
    )
    total_pending_value = (
        (standard_cart_stats["total"] or Decimal("0"))
        + (custom_cart_stats["total"] or Decimal("0"))
    )
    weekly_cart_value = (
        (standard_cart_stats["week"] or Decimal("0"))
        + (custom_cart_stats["week"] or Decimal("0"))
    )
    previous_weekly_cart_value = (
        (standard_cart_stats["previous"] or Decimal("0"))
        + (custom_cart_stats["previous"] or Decimal("0"))
    )
    # Carts holding at least one item of either kind.
    active_cart_count = Cart.objects.filter(
        Exists(CartItem.objects.filter(cart=OuterRef("pk")))
        | Exists(CustomCartItem.objects.filter(cart=OuterRef("pk")))
    ).count()
    weekly_cart_trend = pct_trend(weekly_cart_value, previous_weekly_cart_value)

    # Customers
    customer_stats = Customer.objects.aggregate(
        total=Count("id"),
        period=Count("id", filter=Q(date_joined__gte=period_start_dt)),
    )
    customer_total = customer_stats["total"] or 0
    new_customers_count = customer_stats["period"] or 0
    recent_customers = list(Customer.objects.order_by("-date_joined")[:4])
    for customer in recent_customers:
        display_name = customer.get_full_name().strip() or customer.username
        customer.display_name = display_name
        customer.initials = (
            "".join(part[0] for part in display_name.split()[:2]).upper()
            or customer.username[:2].upper()
        )
    extra_customers = max(customer_total - len(recent_customers), 0)

    # Messages and favorites
    message_stats = ContactMessage.objects.aggregate(
        unread=Count("id", filter=Q(is_read=False)),
        period=Count("id", filter=Q(created_at__gte=period_start_dt)),
    )
    unread_count = message_stats["unread"] or 0
    new_messages_count = message_stats["period"] or 0

    favorite_stats = Favorite.objects.aggregate(
        period=Count("id", filter=Q(created_at__gte=period_start_dt)),
    )
    period_favorites_count = favorite_stats["period"] or 0

    return render(request, "admin/admin-dashboard.html", admin_ctx(
        request, "Dashboard",
        admin_name=admin_name,
        store=store,
        store_is_open=store.status == StoreSettings.Status.OPEN,
        period=period_key,
        period_label=period_label,
        period_choices=period_choices,
        period_start=period_start,
        period_end=period_end,
        product_count=product_count,
        active_product_count=product_stats["active"] or 0,
        low_stock_count=product_stats["low"] or 0,
        out_of_stock_count=product_stats["out"] or 0,
        total_units=total_units,
        inventory_value_display=peso(inventory_value),
        low_stock_products=low_stock_products,
        custom_total_count=custom_total_count,
        custom_total_value_display=peso(custom_total_value),
        custom_period_count=custom_period_count,
        custom_period_value_display=peso(custom_period_value),
        custom_period_trend=custom_period_trend,
        monthly_chart=monthly_chart,
        annual_chart=annual_chart,
        studio_area=studio_area,
        recent_builds=recent_builds,
        weekly_cart_value_display=peso(weekly_cart_value),
        weekly_cart_trend=weekly_cart_trend,
        active_cart_count=active_cart_count,
        total_pending_display=peso(total_pending_value),
        customer_total=customer_total,
        new_customers_count=new_customers_count,
        recent_customers=recent_customers,
        extra_customers=extra_customers,
        unread_count=unread_count,
        new_messages_count=new_messages_count,
        period_favorites_count=period_favorites_count,
    ))
