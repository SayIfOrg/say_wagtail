from django.urls import path
from wagtail import hooks

from .views.views import ProjectListView, change_workon_project


@hooks.register("register_admin_urls")
def register_project_url():
    return [
        path(
            "projects/",
            ProjectListView.as_view(),
            name="project_list",
        ),
        path(
            "projects/set-current-project/<int:project_id>",
            change_workon_project,
            name="project_set_current",
        ),
    ]
