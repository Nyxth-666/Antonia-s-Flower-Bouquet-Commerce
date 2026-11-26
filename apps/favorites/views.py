from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.catalog.models import Bouquet
from .models import Favorite


@login_required
def favorites_page(request):
    favorites = list(
        Favorite.objects.filter(user=request.user).select_related("bouquet")
    )
    favorite_ids = {favorite.bouquet_id for favorite in favorites}
    return render(
        request,
        "favorites/favorites.html",
        {
            "favorites": favorites,
            "favorite_ids": favorite_ids,
        },
    )


@login_required
@require_POST
def toggle_favorite(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, bouquet=bouquet)
    if not created:
        favorite.delete()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "bouquet_id": bouquet.id,
                "is_favorite": created,
            }
        )

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("favorites:favorites")
