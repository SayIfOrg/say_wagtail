from wagtail.users.views.groups import (
    GroupViewSet as WagtailGroupViewSet,
    CreateView as WagtailCreateView,
    DeleteView as WagtailDeleteView,
)

from ..forms import ProjectGroupForm
from ..models import ProjectGroup


class CreateView(WagtailCreateView):
    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        if self.request.method in ("POST", "PUT"):
            kwargs.update({"project": self.request.user.project_user.project})
        return kwargs

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        # Create an object now so that the permission panel forms have something to link them against
        # Change Group() to ProjectGroup() #
        #  #  #  #  #  #  #  #  #  #  #  #
        self.object = ProjectGroup()

        form = self.get_form()
        permission_panels = self.get_permission_panel_forms()
        if form.is_valid() and all(panel.is_valid() for panel in permission_panels):
            response = self.form_valid(form)

            for panel in permission_panels:
                panel.save()

            return response
        else:
            return self.form_invalid(form)


class DeleteView(WagtailDeleteView):
    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data()
        context["group"] = context["projectgroup"]
        return context


class GroupViewSet(WagtailGroupViewSet):
    model = ProjectGroup

    add_view_class = CreateView
    delete_view_class = DeleteView

    def get_form_class(self, for_update=False):
        return ProjectGroupForm
