from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models import UniqueConstraint
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.models import Site


@register_setting
class Project(BaseSiteSetting):
    site = models.OneToOneField(
        Site, related_name="site_project", on_delete=models.PROTECT, primary_key=True
    )


class ProjectUser(models.Model):
    project = models.ForeignKey(
        Project, related_name="project_projectusers", on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_projectusers",
        on_delete=models.PROTECT,
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["project", "user"], name="unique_project_user")
        ]


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.project_user: ProjectUser
