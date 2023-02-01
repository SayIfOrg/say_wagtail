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
                from say.utils.storage import DynamicLibCloudStorage

                storage = DynamicLibCloudStorage(provider_name="minio-static")
            self.instance.file.destination_storage = storage
            return storage


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
                from say.utils.storage import DynamicLibCloudStorage

                storage = DynamicLibCloudStorage(provider_name="minio-static")
            self.instance.file.destination_storage = storage
            return storage
