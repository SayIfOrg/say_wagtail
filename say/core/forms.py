from django import forms
from wagtail.documents.forms import BaseDocumentForm
from wagtail.images.forms import BaseImageForm

from say.storage.models import StorageAccount

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
                storage_account_id = value.split("-")[1]
                storage = StorageAccount.objects.get(
                    pk=storage_account_id
                ).get_storage()
            else:
                from say.core.storage import DynamicLibCloudStorage

                storage = DynamicLibCloudStorage(provider_name="minio-static")
            # The patchy way to set dynamic storage if the save() method did not get called
            self.instance.file.destination_storage = storage
            return storage

    def save(self, commit=True):
        # The patchy way to set dynamic storage in case of the too deep object referencing
        self.instance.file.destination_storage = self.cleaned_data["storage"]
        return super(DSWImageForm, self).save(commit=commit)


class DSWDocumentForm(BaseDocumentForm):
    storage = forms.CharField(max_length=15)

    def __init__(self, *args, user, **kwargs):
        super(DSWDocumentForm, self).__init__(*args, user=user, **kwargs)
        self.fields["storage"].widget = forms.Select(
            choices=get_siteuser_storage_choices(user.site_user.site)
        )

    def clean_storage(self):
        value: str = self.cleaned_data["storage"]
        if value:
            if value != "default":
                storage_account_id = value.split("-")[1]
                storage = StorageAccount.objects.get(
                    pk=storage_account_id
                ).get_storage()
            else:
                from say.core.storage import DynamicLibCloudStorage

                storage = DynamicLibCloudStorage(provider_name="minio-static")
            # The patchy way to set dynamic storage if the save() method did not get called
            self.instance.file.destination_storage = storage
            return storage

    def save(self, commit=True):
        # The patchy way to set dynamic storage in case of the too deep object referencing
        self.instance.file.destination_storage = self.cleaned_data["storage"]
        return super(DSWDocumentForm, self).save(commit=commit)
