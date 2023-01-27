from django import template
from django.utils.translation import gettext as _
from wagtail.models.sites import get_site_user_model

SiteUser = get_site_user_model()


register = template.Library()


@register.filter(name="siteuser_storage_choices")
def get_siteuser_storage_choices(site_user: SiteUser):
    # TODO
    other_storages = [("default", _("The default storage"))]
    return other_storages
