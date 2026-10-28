from apps.core.data.navbar import (
    NAVBAR_LINKS,
    NAVBAR_ICONS,
    NAVBAR_SEARCH,
)
from apps.core.data.footer import FOOTER_LINKS
from apps.catalog.data.flower_type import FLOWER_TYPE
from apps.catalog.data.arrangement_type import ARRANGEMENT_TYPES
from apps.occasions.data.occasions import OCCASIONS

def navbar_data(request):
    return {
        "navbar_links": NAVBAR_LINKS,
        "navbar_icons": NAVBAR_ICONS,
        "navbar_search": NAVBAR_SEARCH,
        "footer_links": FOOTER_LINKS,
        "flower_types": FLOWER_TYPE,
        "arrangement_types": ARRANGEMENT_TYPES,
        "occasions": OCCASIONS,
    }
