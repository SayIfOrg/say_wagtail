import re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from user_manager.models import ProjectUser
from user_manager.utils import set_current_session_project


class ProjectUserMiddleware(MiddlewareMixin):
    """
    Middleware that sets `site` attribute to request object and `project_user` attribute to user object.
    It should be located after user is set to request(after `AuthenticationMiddleware`)
    """

    def process_request(self, request):
        if not request.user.is_authenticated:
            # The hole point is to be able to handle user permissions,
            # so if not `is_authenticated` the view should trigger it
            return
        paths = getattr(settings, "PATHS_NEED_SITE", None)
        if not paths:
            # The urls that not included but need this behavior
            # should use `set_current_project_site` decorator
            return
        if any([re.match(pattern, request.path) for pattern in paths]):
            project_id = request.session.get("project_id")
            if not project_id:
                project_id = request.session[
                    "project_id"
                ] = request.user.user_projectusers.last().project_id
            project_user = (
                ProjectUser.objects.filter(
                    project_id=project_id, user_id=request.user.id
                )
                .select_related("project__site")
                .get()
            )
            set_current_session_project(request, project_user)
