from django.forms import Media
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from wagtail.admin.ui.tables import Column, TitleColumn
from wagtail.admin.views.generic.chooser import (
    BaseChooseView,
    ChooseViewMixin,
    ChooseResultsViewMixin,
    ChosenResponseMixin,
    ChosenViewMixin,
    CreationFormMixin,
)
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.widgets import BaseChooser

from linked_account.components import TelegramInstancePanel, TelegramInstanceCreatePanel


@method_decorator(csrf_exempt, name="dispatch")
class TelegramLinkedAccountView(View):
    def get(self, request):
        from linked_account.models import TelegramInstance

        instances = [
            {"id": i.id, "title": i.title, "type": i.type}
            for i in TelegramInstance.all()
        ]

        panels = [
            TelegramInstanceCreatePanel(request.path, "post"),
            TelegramInstancePanel(instances),
        ]
        media = Media()
        for panel in panels:
            media += panel.media
        return render(
            request,
            "linked_account/list.html",
            {"panels": panels, "media": media},
        )

    def post(self, request):
        return TelegramInstanceCreatePanel.callback(request)


class BaseTelegramInstanceChooseView(BaseChooseView):
    @property
    def columns(self):
        return [
            TitleColumn(
                "title",
                label=_("Title"),
                accessor="title",
                id_accessor="id",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            Column("type", label=_("Type"), accessor="type"),
        ]

    def get_object_list(self):
        from linked_account.models import TelegramInstance

        return [
            {"id": i.id, "title": i.title, "type": i.type}
            for i in TelegramInstance.all()
        ]

    def apply_object_list_ordering(self, objects):
        return objects


class TelegramInstanceChooseView(
    ChooseViewMixin, CreationFormMixin, BaseTelegramInstanceChooseView
):
    pass


class TelegramInstanceChooseResultsView(
    ChooseResultsViewMixin, CreationFormMixin, BaseTelegramInstanceChooseView
):
    pass


class TelegramInstanceChosenViewMixin(ChosenViewMixin):
    def get_object(self, pk):
        from linked_account.models import TelegramInstance

        r = TelegramInstance.get(int(pk))
        return {"id": r.id, "title": r.title, "type": r.type}


class TelegramInstanceChosenResponseMixin(ChosenResponseMixin):
    def get_chosen_response_data(self, item):
        return {
            "id": item["id"],
            "title": item["title"],
        }


class TelegramInstanceChosenView(
    TelegramInstanceChosenViewMixin, TelegramInstanceChosenResponseMixin, View
):
    pass


class BaseTelegramInstanceChooserWidget(BaseChooser):
    def get_instance(self, value):
        if value is None:
            return None
        elif isinstance(value, dict):
            return value
        else:
            from linked_account.models import TelegramInstance

            r = TelegramInstance.get(int(value))
            return {"id": r.id, "title": r.title, "type": r.type}

    def get_value_data_from_instance(self, instance):
        return {
            "id": instance["id"],
            "title": instance["title"],
        }


class TelegramInstanceChooserViewSet(ChooserViewSet):
    icon = "user"
    choose_one_text = "Choose a telegram instance"
    choose_another_text = "Choose telegram instance"
    edit_item_text = "Edit this telegram instance"

    choose_view_class = TelegramInstanceChooseView
    choose_results_view_class = TelegramInstanceChooseResultsView
    chosen_view_class = TelegramInstanceChosenView
    base_widget_class = BaseTelegramInstanceChooserWidget


telegram_instance_chooser_viewset = TelegramInstanceChooserViewSet(
    "telegram_instance_chooser", url_prefix="telegram-instance-chooser"
)
