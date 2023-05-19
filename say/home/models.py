from django.db import models
from wagtail.models import Page

from wagtail_headless_preview.models import HeadlessMixin


class HomePage(HeadlessMixin, Page):
    parent_page_types = ["wagtailcore.Page"]
