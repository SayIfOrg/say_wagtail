from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from grapple.models import GraphQLStreamfield


class SimplePage(Page):
    body = StreamField(
        [
            ("editor", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    graphql_fields = [
        GraphQLStreamfield("body"),
    ]
