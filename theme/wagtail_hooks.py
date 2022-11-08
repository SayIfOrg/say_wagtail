from django.template.loader import render_to_string
from wagtail import hooks

from tailwind.templatetags.tailwind_tags import tailwind_css


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return render_to_string("tailwind/tags/css.html", context=tailwind_css())
