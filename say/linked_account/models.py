from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin.panels import FieldPanel, FieldRowPanel, PageChooserPanel
from wagtail.admin.widgets import SwitchInput
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet

import grpc
from modelcluster.fields import ParentalKey
from say_protos import webpage_pb2, webpage_pb2_grpc

from say.linked_account.views import telegram_instance_chooser_viewset


class TelegramActionForm(WagtailAdminModelForm):
    telegram_instance = forms.IntegerField(
        widget=telegram_instance_chooser_viewset.widget_class
    )

    def __init__(self, *args, **kwargs):
        super(TelegramActionForm, self).__init__(*args, **kwargs)
        self.fields["telegram_instance"].initial = 1

    def clean_telegram_instance(self):
        value = self.cleaned_data.get("telegram_instance")
        return value


class TelegramAction(Orderable):
    base_form_class = TelegramActionForm
    page = ParentalKey(
        "page_types.SimplePage",
        related_name="page_telegramactions",
        on_delete=models.CASCADE,
    )
    telegram_publish_mode = models.ForeignKey(
        "linked_account.TelegramPublishMode", on_delete=models.CASCADE
    )

    panels = [
        PageChooserPanel("page"),
        FieldPanel("telegram_instance"),
        FieldPanel("telegram_publish_mode"),
    ]


@register_snippet
class TelegramPublishMode(models.Model):
    class ReferenceToMessage(models.IntegerChoices):
        NO_REFERENCE = 0, _("No reference")
        LINK = 1, _("Link")
        REPLY = 2, _("Reply")

    title = models.CharField(
        max_length=63, help_text=_("The title for you to recognize this action")
    )
    publish_message = models.BooleanField(
        help_text=_("Incase of first publish(create) the content: Send new message?")
    )
    republish_message = models.BooleanField(
        help_text=_("Incase of republish(edit) the content: Send new message?")
    )
    edit_past_messages = models.BooleanField(
        help_text=_(
            "Incase of republish(edit) the content: Edit previously sent messages?"
        )
    )
    as_reference_to_original_message = models.PositiveSmallIntegerField(
        choices=ReferenceToMessage.choices,
        default=ReferenceToMessage.NO_REFERENCE,
        help_text=_(
            "Incase of republish(edit) the content: How to mention original sent message?"
        ),
    )

    panels = [
        FieldPanel("title"),
        FieldRowPanel(
            [
                FieldPanel("publish_message", widget=SwitchInput),
                FieldPanel("republish_message", widget=SwitchInput),
                FieldPanel("edit_past_messages", widget=SwitchInput),
            ],
            heading=_("Functionalities"),
        ),
        FieldRowPanel(
            [
                FieldPanel("as_reference_to_original_message"),
            ]
        ),
    ]

    def __str__(self):
        return self.title


class TelegramInstance:
    @staticmethod
    def all() -> webpage_pb2.Instances:
        with grpc.insecure_channel("say-telegram-grpc:5060") as channel:
            stub = webpage_pb2_grpc.ManageInstanceStub(channel)
            r = stub.InstanceList(webpage_pb2.Project(id=1, name=""))
            return r.instances

    @staticmethod
    def get(pk: int) -> webpage_pb2.Instance:
        with grpc.insecure_channel("say-telegram-grpc:5060") as channel:
            stub = webpage_pb2_grpc.ManageInstanceStub(channel)
            r = stub.InstanceDetail(webpage_pb2.Instance(id=pk))
            return r
