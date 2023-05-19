from django import forms
from django.db import models
from django.db.models import Exists, OuterRef
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from grapple.models import GraphQLPage, GraphQLStreamfield
from modelcluster.fields import ParentalManyToManyField
from wagtail_headless_preview.models import HeadlessMixin


class ListablePageMixin(models.Model):
    listings = ParentalManyToManyField(
        "ListingPage",
        related_name="listingpage_%(class)ss",
        blank=True,
        help_text=_("A reference to this page appear in witch ListablePages"),
    )

    class Meta:
        abstract = True

    graphql_fields = [
        GraphQLPage("listings", is_list=True),
    ]


class SimplePage(
    HeadlessMixin,
    Page,
    ListablePageMixin,
):
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

    graphql_fields = ListablePageMixin.graphql_fields + [
        GraphQLStreamfield("body"),
    ]


class ListingPage(HeadlessMixin, Page):
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

    def listingpage_pages(self, info, **kwargs):
        """
        Add other types of listables here
        """
        simple_page = self.listingpage_simplepages.filter(id__in=OuterRef("pk"))
        return Page.objects.filter(Exists(simple_page)).specific()

    graphql_fields = [
        GraphQLStreamfield("body"),
        GraphQLPage("listingpage_simplepages", is_list=True),
        GraphQLPage("listingpage_pages", is_list=True),
    ]
