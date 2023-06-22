from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from wagtail.models.sites import get_site_user_model

from .models import Project


User = get_user_model()
SiteUser = get_site_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(SiteUser)
class SiteUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
