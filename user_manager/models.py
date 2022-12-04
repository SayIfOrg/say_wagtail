from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,
    Permission,
    GroupManager,
    _user_get_permissions,
    _user_has_perm,
    _user_has_module_perms,
)
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.itercompat import is_iterable
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.models import Site


@register_setting
class Project(BaseSiteSetting):
    site = models.OneToOneField(
        Site, related_name="site_project", on_delete=models.PROTECT, primary_key=True
    )


class ProjectGroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name, project_id):
        return self.get(name=name, project_id=project_id)


class ProjectGroup(models.Model):
    """
    ProjectGroup are a generic way of categorizing project_users to apply permissions, or
    some other label, to those users.
    """

    name = models.CharField(_("name"), max_length=150)
    permissions = models.ManyToManyField(
        Permission,
        related_name="permission_projectgroups",
        verbose_name=_("permissions"),
        blank=True,
    )
    project = models.ForeignKey(
        Project, related_name="project_projectgroups", on_delete=models.CASCADE
    )

    objects = GroupManager()

    class Meta:
        swappable = "AUTH_GROUP_MODEL"
        verbose_name = _("group")
        verbose_name_plural = _("groups")

        constraints = [
            UniqueConstraint(fields=["name", "project"], name="unique_name_project")
        ]

    @property
    def user_set(self):
        return self.projectgroup_projectusers

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name, self.project_id


class ProjectUser(models.Model):
    project = models.ForeignKey(
        Project, related_name="project_projectusers", on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_projectusers",
        on_delete=models.PROTECT,
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )

    groups = models.ManyToManyField(
        ProjectGroup,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="projectgroup_projectusers",
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="permission_projectusers",
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["project", "user"], name="unique_project_user")
        ]

    def get_project_user_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has directly.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "user")

    def get_project_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "group")

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        if not is_iterable(perm_list) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.project_user: ProjectUser
