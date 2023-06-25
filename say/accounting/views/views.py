import os

from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from wagtail.admin import messages
from wagtail.images import get_image_model
from wagtail.models.sites import Site, get_site_user_model
from wagtail.sites.utils import set_current_session_project

from say.accounting.models import CustomUserProfile
from say.core.storage import DynamicLibCloudStorage


UserModel = get_user_model()
SiteUser = get_site_user_model()
ImageModel = get_image_model()


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


@csrf_exempt
@require_POST
def avatar_view(request, user_id):
    user = get_object_or_404(UserModel, pk=user_id)
    if not hasattr(user, "user_customuserprofile"):
        CustomUserProfile.objects.create(user=user)
    file = request.FILES["avatar"]
    with transaction.atomic():
        avatar = ImageModel(file=file, uploaded_by_user_id=1)
        avatar.file.destination_storage = DynamicLibCloudStorage(
            provider_name="minio-1"
        )
        avatar.file.save(os.path.basename(file.name), avatar.file.file, save=False)
        avatar._set_image_file_metadata()
        avatar.save()
        user.user_customuserprofile.avatar = avatar
        user.user_customuserprofile.save()
    return JsonResponse({"status": "ok"}, status=201)
