from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks

from tailwind.templatetags.tailwind_tags import tailwind_css


tailwind_content = render_to_string("tailwind/tags/css.html", context=tailwind_css())
flowbite_content = format_html('<script src="{}"></script>', static("js/vendor/flowbite.js"))
htmx_content = format_html('<script src="{}" defer></script>', static("js/vendor/htmx.min.js"))


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return "/n".join((tailwind_content,))


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return "".join((flowbite_content, htmx_content))
