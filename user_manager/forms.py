from django import forms
from wagtail.models import SiteGroup
from wagtail.users.forms import GroupForm as WagtailGroupForm


class SiteGroupForm(WagtailGroupForm):
    def __init__(self, *args, site=None, **kwargs):
        super(SiteGroupForm, self).__init__(*args, **kwargs)
        self.site = site

    class Meta:
        model = SiteGroup
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
            self.instance.site = self.site
        project_group = super(SiteGroupForm, self).save(commit=commit)
        project_group.permissions.add(*untouchable_permissions)
        return project_group
