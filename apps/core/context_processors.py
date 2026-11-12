from apps.core.data.navbar import (
    NAVBAR_LINKS,
    NAVBAR_ICONS,
    NAVBAR_SEARCH,
)
from apps.core.data.footer import FOOTER_LINKS
from apps.catalog.models import FlowerType
from apps.catalog.models import ArrangementType
from apps.catalog.models import Occasion

def navbar_data(request):
    return {
        "navbar_links": NAVBAR_LINKS,
        "navbar_icons": NAVBAR_ICONS,
        "navbar_search": NAVBAR_SEARCH,
        "footer_links": FOOTER_LINKS,
        
        "flower_types": FlowerType.objects.filter(is_active=True),
        "arrangement_types": ArrangementType.objects.filter(is_active=True),
        "occasions": Occasion.objects.filter(is_active=True),
    }
