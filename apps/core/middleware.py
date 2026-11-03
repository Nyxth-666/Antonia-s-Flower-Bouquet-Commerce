import os

from django.conf import settings
from django.contrib.auth import logout

SESSION_KEY = "dev_boot_id"


class DevLogoutOnStartupMiddleware:
    """
    DEV ONLY (DEBUG=True): log everyone out each time `runserver` is started.

    settings.py creates one DEV_BOOT_ID per runserver command. Each browser
    session is stamped with it. A session with no stamp, or an old stamp,
    comes from a previous run, so we log that user out.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        boot_id = os.environ.get("DEV_BOOT_ID")
        
        if settings.DEBUG and boot_id:
            if request.session.get(SESSION_KEY) != boot_id:
                if request.user.is_authenticated:
                    logout(request)
                request.session[SESSION_KEY] = boot_id

        return self.get_response(request)