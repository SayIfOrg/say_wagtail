from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import ObjectList, TabbedInterface
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from grapple.models import GraphQLStreamfield


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

    # social_media_panels = [
    #     FormableInlinePanel(
    #         "page_telegramactions", form=TelegramActionForm, label="Telegram actions"
    #     ),
    # ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
            # ObjectList(social_media_panels, heading=_("Social media")),
            ObjectList(Page.promote_panels, heading=_("Promote")),
            ObjectList(
                Page.settings_panels, heading=_("Settings"), classname="settings"
            ),
        ]
    )

    api_fields = [
        APIField("body"),
    ]

    graphql_fields = [
        GraphQLStreamfield("body"),
    ]
