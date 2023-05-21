from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from grapple.models import GraphQLPage, GraphQLStreamfield
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail_headless_preview.models import HeadlessMixin

from say.page_types.forms import SimplePageForm


class GeneralManyPage(ClusterableModel):
    rel1 = ParentalKey(
        "wagtailcore.Page", on_delete=models.CASCADE, related_name="r1_generals"
    )
    rel2 = ParentalKey(
        "wagtailcore.Page", on_delete=models.CASCADE, related_name="r2_generals"
    )

    class Type(models.IntegerChoices):
        SIMPLE_LISTING = 101, _("pages that appear in ListingPages")

    type = models.PositiveSmallIntegerField(choices=Type.choices)


class GeneralPageListingManager(models.Manager):
    @staticmethod
    def get_listed_in(page: Page):
        """returns pages that the page is listed in"""
        return Page.objects.filter(
            r1_generals__type=GeneralManyPage.Type.SIMPLE_LISTING,
            r1_generals__rel2_id=page.pk,
        )

    @staticmethod
    def set_listings(page, pages):
        """adds the page to the pages listings list, call save on page your self"""
        general_many_pages = []
        for listing_page in pages:
            general_many_pages.append(
                GeneralPageListing(
                    rel1_id=listing_page.pk, type=GeneralManyPage.Type.SIMPLE_LISTING
                )
            )
        page.r2_generals = general_many_pages

    @staticmethod
    def get_listed_pages(page):
        """returns pages that are registered to be listed on page"""
        return Page.objects.filter(
            r2_generals__type=GeneralManyPage.Type.SIMPLE_LISTING,
            r2_generals__rel1_id=page.id,
        ).specific()


class GeneralPageListing(GeneralManyPage):
    objects = GeneralPageListingManager()

    class Meta:
        proxy = True


class SimplePage(
    HeadlessMixin,
    Page,
):
    base_form_class = SimplePageForm
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
            [FieldPanel("listings")],
            _("Include in ListablePages"),
        ),
    ]

    graphql_fields = [
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

    def listed_pages(self, info, **kwargs):
        return GeneralPageListing.objects.get_listed_pages(self)

    graphql_fields = [
        GraphQLStreamfield("body"),
        GraphQLPage("listed_pages", is_list=True),
    ]
