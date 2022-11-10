from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView
from wagtail.admin import messages

from .models import Project, ProjectUser
from .utils import set_current_session_project


class ProjectListView(ListView):
    def get_template_names(self):
        if self.request.htmx or self.request.GET.get("htmx"):
            return "user_manager/partial_components/project_list.html"
        raise Http404()

    def get_queryset(self):
        return Project.objects.filter(project_projectusers__user=self.request.user)


def change_workon_project(request, project_id):
    try:
        project_user = request.user.user_projectusers.get(project_id=project_id)
    except ProjectUser.DoesNotExist:
        messages.error(
            request, _("This project does not exists or you are not a part of it.")
        )
    else:
        set_current_session_project(request, project_user)
        messages.success(
            request,
            _(
                "You are now working on {project_name}".format(
                    project_name=request.user.project_user.project
                )
            ),
        )

    if request.htmx:
        resp = HttpResponse()
        resp["HX-Refresh"] = "true"
    else:
        resp = redirect(request.META["HTTP_REFERER"])
    return resp
