from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StreamValue
from wagtail.core.models import Page
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

StreamValue
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
