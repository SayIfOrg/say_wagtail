def set_current_session_project(request, project_user):
    request.session["project_id"] = project_user.project_id
    request.user.project_user = project_user
    request._wagtail_site = project_user.project.site
