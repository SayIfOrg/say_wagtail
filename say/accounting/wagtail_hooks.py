from django.urls import path
from wagtail import hooks

from .views.linking import linking_telebot
from .views.views import SiteChooserView, set_workon_site


@hooks.register("register_admin_urls")
def extra_sites_urls():
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


@hooks.register("register_admin_urls")
def linking_urls():
    return [
        path(
            "linking/telebot/<str:botel_username>/",
            linking_telebot,
            name="linking_telebot",
        ),
    ]
