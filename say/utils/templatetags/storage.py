from django import template
from django.utils.translation import gettext as _
from wagtail.models.sites import get_site_user_model

from say.storage.models import StorageAccount

SiteUser = get_site_user_model()


register = template.Library()

STORAGE_ACCOUNT_PREFIX = "sa"


@register.filter(name="siteuser_storage_choices")
def get_siteuser_storage_choices(site_user: SiteUser):
    # TODO
    storage_accounts = StorageAccount.objects.all()
    other_storages = [("default", _("The default storage"))]
    storage_accounts = [
        (f"{STORAGE_ACCOUNT_PREFIX}-{i.pk}", i.title) for i in storage_accounts
    ]
    return other_storages + storage_accounts
