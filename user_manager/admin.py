from django.contrib import admin

from .models import ProjectUser, Project


@admin.register(ProjectUser)
class ProjectUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

