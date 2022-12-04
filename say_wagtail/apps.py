from wagtail.users.apps import WagtailUsersAppConfig


class CustomUsersAppConfig(WagtailUsersAppConfig):
    group_viewset = "user_manager.views.groups.GroupViewSet"
