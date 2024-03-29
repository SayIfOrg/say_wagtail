from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem

from .views import TelegramLinkedAccountView, telegram_instance_chooser_viewset


@hooks.register("register_admin_urls")
def register_calendar_url():
    return [
        path(
            "telegram-linked-account/",
            TelegramLinkedAccountView.as_view(),
            name="telegram_linked_account",
        ),
    ]


@hooks.register("register_admin_menu_item")
def register_calendar_menu_item():
    submenu = Menu(
        items=[
            MenuItem(
                _("Telegram instances"),
                reverse("telegram_linked_account"),
                icon_name="date",
            ),
        ]
    )

    return SubmenuMenuItem(_("Linked accounts"), submenu, classnames="icon icon-date")


@hooks.register("register_admin_viewset")
def register_viewset():
    return telegram_instance_chooser_viewset
