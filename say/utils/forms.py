from django import forms
from wagtail.images.forms import BaseImageForm

from .templatetags.storage import get_siteuser_storage_choices


class DSWImageForm(BaseImageForm):
    storage = forms.CharField(max_length=15)

    def __init__(self, *args, user, **kwargs):
        super(DSWImageForm, self).__init__(*args, user=user, **kwargs)
        self.fields["storage"].widget = forms.Select(
            choices=get_siteuser_storage_choices(user.site_user.site)
        )

    def clean_storage(self):
        value: str = self.cleaned_data["storage"]
        if value:
            if value != "default":
                # TODO
                raise NotImplementedError
            else:
                from .storage import DynamicLibCloudStorage

                storage = DynamicLibCloudStorage(provider_name="minio-static")
            self.instance.file.destination_storage = storage
            return storage
