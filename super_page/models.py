from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.edit_handlers import ObjectList, TabbedInterface
from wagtail.admin.panels import MultiFieldPanel, FieldPanel, FieldRowPanel, InlinePanel
from wagtail.admin.widgets import SwitchInput
from wagtail.core.models import Page
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey


class SimplePage(Page):
    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    social_media_panels = [
        InlinePanel("page_telegramactions", label="Telegram actions"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
            ObjectList(social_media_panels, heading=_("Social media")),
            ObjectList(Page.promote_panels, heading=_("Promote")),
            ObjectList(
                Page.settings_panels, heading=_("Settings"), classname="settings"
            ),
        ]
    )


from wagtail.log_actions import log


class TelegramActionOrderable(Orderable):
    page = ParentalKey(
        "super_page.SimplePage",
        related_name="page_telegramactions",
        on_delete=models.CASCADE,
    )
    telegram_instance = models.ForeignKey(
        "super_page.TelegramInstance", on_delete=models.CASCADE
    )
    telegram_publish_mode = models.ForeignKey(
        "super_page.TelegramPublishMode", on_delete=models.CASCADE
    )

    panels = [
        SnippetChooserPanel("telegram_instance"),
        FieldPanel("telegram_publish_mode"),
    ]


class TelegramInstance(models.Model):
    class Type(models.IntegerChoices):
        GROUP = 1, _("Group")
        CHANNEL = 2, _("Channel")

    type = models.PositiveSmallIntegerField(choices=Type.choices)
    chat_id = models.PositiveIntegerField()


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
    # from wagtail.admin.widgets import
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
