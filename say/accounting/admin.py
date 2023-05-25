from django.contrib import admin
from wagtail.models.sites import get_site_user_model

from .models import Project


SiteUser = get_site_user_model()


@admin.register(SiteUser)
class ProjectUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
