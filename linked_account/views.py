import grpc
from django.shortcuts import render
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

from say_wagtail.grpc import webpage_pb2_grpc, webpage_pb2


def telegram_linked_account(request):
    return render(request, "linked_account/list.html", {})


class BaseUserChooseView(BaseChooseView):
    @property
    def columns(self):
        return [
            TitleColumn(
                "title",
                label="Title",
                accessor="title",
                id_accessor="id",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            Column("type", label="Type", accessor="type"),
        ]

    def get_object_list(self):
        with grpc.insecure_channel("localhost:5060") as channel:
            stub = webpage_pb2_grpc.ManageInstanceStub(channel)
            r = stub.InstanceList(webpage_pb2.Project(id=1, name=""))
            return [{"id": i.id, "title": i.title, "type": i.type} for i in r.instances]

    def apply_object_list_ordering(self, objects):
        return objects


class TelegramInstanceChooseView(
    ChooseViewMixin, CreationFormMixin, BaseUserChooseView
):
    pass


class TelegramInstanceChooseResultsView(
    ChooseResultsViewMixin, CreationFormMixin, BaseUserChooseView
):
    pass


class TelegramInstanceChosenViewMixin(ChosenViewMixin):
    def get_object(self, pk):
        with grpc.insecure_channel("localhost:5060") as channel:
            stub = webpage_pb2_grpc.ManageInstanceStub(channel)
            r = stub.InstanceDetail(webpage_pb2.Instance(id=int(pk)))
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
            with grpc.insecure_channel("localhost:5060") as channel:
                stub = webpage_pb2_grpc.ManageInstanceStub(channel)
                r = stub.InstanceDetail(webpage_pb2.Instance(id=int(value)))
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
