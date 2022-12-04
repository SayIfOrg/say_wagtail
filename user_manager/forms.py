from django import forms
from wagtail.users.forms import GroupForm as WagtailGroupForm

from .models import ProjectGroup


class ProjectGroupForm(WagtailGroupForm):
    def __init__(self, *args, project=None, **kwargs):
        super(ProjectGroupForm, self).__init__(*args, **kwargs)
        self.project = project

    class Meta:
        model = ProjectGroup
        fields = (
            "name",
            "permissions",
        )
        widgets = {
            "permissions": forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True):
        try:
            untouchable_permissions = self.instance.permissions.exclude(
                pk__in=self.registered_permissions
            )
            bool(
                untouchable_permissions
            )  # force this to be evaluated, as it's about to change
        except ValueError:
            # this form is not bound; we're probably creating a new group
            untouchable_permissions = []
        if not self.instance.pk:
            self.instance.project = self.project
        project_group = super(ProjectGroupForm, self).save(commit=commit)
        project_group.permissions.add(*untouchable_permissions)
        return project_group
