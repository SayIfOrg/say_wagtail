from django.db import models
from wagtail.models import Page


class HomePage(Page):
    parent_page_types = ["wagtailcore.Page"]
