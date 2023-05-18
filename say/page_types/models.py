from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.fields import StreamField
from wagtail.models import Page

from modelcluster.fields import ParentalManyToManyField
from grapple.models import GraphQLStreamfield, GraphQLPage


class ListablePage(Page):
    max_count = 0

    listings = ParentalManyToManyField(
        "ListingPage",
        related_name="listingpage_pages",
        blank=True,
        help_text=_("A reference to this page appear in witch ListablePages"),
    )

    graphql_fields = [
        GraphQLPage("listingpage_pages", is_list=True),
    ]


class SimplePage(ListablePage):
    max_count = None  # set to default
    parent_page_types = ["home.HomePage", "SimplePage"]

    body = StreamField(
        [
            ("editor", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [FieldPanel("listings", widget=forms.CheckboxSelectMultiple)],
            _("Include in ListablePages"),
        ),
    ]

    graphql_fields = [
        GraphQLStreamfield("body"),
        GraphQLPage("listings", is_list=True),
    ]


class ListingPage(Page):
    body = StreamField(
        [
            ("editor", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    graphql_fields = ListablePage.graphql_fields + [
        GraphQLStreamfield("body"),
    ]
