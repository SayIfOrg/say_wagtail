from django.urls import path
from wagtail import hooks

from .views.views import SiteChooserView, set_workon_site


@hooks.register("register_admin_urls")
def register_project_url():
    return [
        path(
            "sites/chooser-list",
            SiteChooserView.as_view(),
            name="site_chooser_list",
        ),
        path(
            "sites/set-current-project/<int:site_id>",
            set_workon_site,
            name="set_workon_site",
        ),
    ]
