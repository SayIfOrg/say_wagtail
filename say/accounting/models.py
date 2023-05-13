from django.contrib.auth.models import (
    AbstractUser,
    UserManager as BaseUserManager,
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


class UserQuerySet(models.QuerySet):
    def for_site(self, site: Site):
        return self.filter(user_siteusers__site=site)


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)


class User(SitePermissionsMonkeyPatchMixin, AbstractUser):
    IN_SITE_METHOD = "for_site"
    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.site_user: SiteUser