from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView
from wagtail.admin import messages
from wagtail.models.sites import get_site_user_model, Site
from wagtail.sites.utils import set_current_session_project

SiteUser = get_site_user_model()


class SiteChooserView(ListView):
    model = Site

    def get_template_names(self):
        if self.request.htmx or self.request.GET.get("htmx"):
            return "accounting/partial_components/site_list.html"
        raise Http404()

    def get_queryset(self):
        return (
            super(SiteChooserView, self)
            .get_queryset()
            .filter(
                site_siteusers__id__in=SiteUser.objects.all().siteusers_to_manage(
                    self.request.user
                )
            )
        )


def set_workon_site(request, site_id):
    try:
        site_user = (
            SiteUser.objects.all()
            .siteusers_to_manage(request.user)
            .get(site_id=site_id)
        )
    except SiteUser.DoesNotExist:
        messages.error(
            request, _("This project does not exists or you are not a part of it.")
        )
    else:
        set_current_session_project(request, site_user)
        messages.success(
            request,
            _(
                "You are now working on {site_name}".format(
                    site_name=request.user.site_user.site.site_name
                    or request.user.site_user.site.sitename
                )
            ),
        )

    if request.htmx:
        resp = HttpResponse()
        resp["HX-Refresh"] = "true"
    else:
        resp = redirect(request.META["HTTP_REFERER"])
    return resp
