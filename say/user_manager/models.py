from django.contrib.auth.models import (
    AbstractUser,
)
from django.db import models
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.models import Site
from wagtail.models.sites import AbstractSiteUser
from wagtail.sites.utils import SitePermissionsMonkeyPatchMixin


@register_setting
class Project(BaseSiteSetting):
    site = models.OneToOneField(
        Site, related_name="site_project", on_delete=models.PROTECT, primary_key=True
    )


class SiteUser(AbstractSiteUser):
    pass


class User(SitePermissionsMonkeyPatchMixin, AbstractUser):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.site_user: SiteUser
