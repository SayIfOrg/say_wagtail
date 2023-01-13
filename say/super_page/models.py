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

from say.linked_account.models import TelegramActionForm


class FormableInlinePanel(InlinePanel):
    def __init__(self, relation_name, form=None, *args, **kwargs):
        self.form = form
        super(FormableInlinePanel, self).__init__(relation_name, *args, **kwargs)

    def clone_kwargs(self):
        kwargs = super(FormableInlinePanel, self).clone_kwargs()
        kwargs.update(form=self.form)
        return kwargs

    def get_form_options(self):
        form_options = super(FormableInlinePanel, self).get_form_options()
        form_options["formsets"][self.relation_name].update(form=self.form)
        return form_options


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
        FormableInlinePanel(
            "page_telegramactions", form=TelegramActionForm, label="Telegram actions"
        ),
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
