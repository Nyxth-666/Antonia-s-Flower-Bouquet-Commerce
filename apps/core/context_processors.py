from apps.core.data.navbar import (
    NAVBAR_LINKS,
    NAVBAR_ICONS,
    NAVBAR_SEARCH,
)
from apps.core.data.footer import FOOTER_LINKS

def navbar_data(request):
    return {
        "navbar_links": NAVBAR_LINKS,
        "navbar_icons": NAVBAR_ICONS,
        "navbar_search": NAVBAR_SEARCH,
        "footer_links": FOOTER_LINKS
    }
