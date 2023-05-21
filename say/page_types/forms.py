from django import forms
from django.utils.translation import gettext as _
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.models import Page


class SimplePageForm(WagtailAdminPageForm):
    listings = forms.ModelMultipleChoiceField(
        queryset=Page.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text=_("A reference to this page appear in witch ListablePages"),
    )

    def __init__(self, *args, **kwargs):
        from say.page_types.models import ListingPage

        super(SimplePageForm, self).__init__(*args, **kwargs)
        self.fields["listings"].queryset = ListingPage.objects.in_site(
            self.for_user.site_user.site
        )
        if self.instance and self.instance.pk:
            from say.page_types.models import GeneralPageListing

            self.initial.update(
                {
                    "listings": GeneralPageListing.objects.get_listed_in(
                        self.instance
                    ).type(ListingPage)
                }
            )

    def save(self, commit=True):
        from say.page_types.models import GeneralPageListing

        GeneralPageListing.objects.set_listings(
            self.instance, self.cleaned_data["listings"]
        )
        return super(SimplePageForm, self).save(commit)
