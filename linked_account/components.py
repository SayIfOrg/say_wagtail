from typing import Mapping, Any

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
from wagtail.admin.ui.components import Component


class TelegramInstancePanel(Component):
    template_name = "linked_account/panels/telegram_instance.html"

    def __init__(self, instances):
        self.instances = instances

    def get_context_data(self, parent_context: Mapping[str, Any]) -> Mapping[str, Any]:
        context = super(TelegramInstancePanel, self).get_context_data(parent_context)
        context["instances"] = self.instances
        return context

    class Media:
        css = {"all": ("css/vendor/bootstrap.min.css",)}
        js = ("js/vendor/bootstrap.bundle.min.js",)


class TelegramInstanceCreatePanel(Component):
    template_name = "linked_account/panels/telegram_instance_create.html"

    def __init__(self, url, callback_method):
        self.url = url
        self.callback_method = callback_method

    def get_context_data(self, parent_context: Mapping[str, Any]) -> Mapping[str, Any]:
        context = super(TelegramInstanceCreatePanel, self).get_context_data(
            parent_context
        )
        context["url"] = self.url
        context["callback_method"] = self.callback_method
        return context

    class Media:
        css = {"all": ("css/vendor/bootstrap.min.css",)}
        js = ("js/vendor/bootstrap.bundle.min.js",)

    @staticmethod
    def callback(request):
        if request.POST.get("new"):
            from secrets import token_hex

            code = token_hex(5).upper()
            cache.set(1, code, 180)
            cache.set(code, 1, 180)
            return JsonResponse({"code": code}, status=status.HTTP_200_OK)
        elif code := request.POST.get("code"):
            if cache.get(1) != code:
                return JsonResponse(
                    {"message": "expired_or_not_existed"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if cache.get(code) == "commit":
                return JsonResponse({"message": "done"}, status=status.HTTP_201_CREATED)
            return JsonResponse(
                {"message": "not_yet"}, status=status.HTTP_204_NO_CONTENT
            )
