from apps.core.data.navbar import (
    NAVBAR_LINKS,
    NAVBAR_ICONS,
    NAVBAR_SEARCH,
)

def navbar_data(request):
    return {
        "navbar_links": NAVBAR_LINKS,
        "navbar_icons": NAVBAR_ICONS,
        "navbar_search": NAVBAR_SEARCH,
    }
