from django.conf import settings
from wagtail.models import Site


def get_client_site_root_url(site: Site):
    return f"{settings.WEBFACE_URL.geturl()}/@{site.sitename}"
