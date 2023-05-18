from abc import abstractmethod
from typing import Any, Iterable, Mapping

from django import forms
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.files.base import ContentFile, File
from django.core.files.storage import Storage
from django.core.validators import integer_validator
from django.forms.models import construct_instance
from django.utils.translation import gettext as _
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin.panels import FieldPanel, ObjectList

from .models import AVAILABLE_STORAGES, StorageAccount
from .storage import Minio2AccountStorage, MinioAccountStorage, get_storage_by_identity


class StorageAccountBaseAdminModelForm(WagtailAdminModelForm):
    EMPTY_TYPE = [("", _("Choose a storage"))]
    TYPE_CHOICES = EMPTY_TYPE + [(i.IDENTITY, i.title()) for i in AVAILABLE_STORAGES]
    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(
            attrs={
                "hx-get": "",
                "hx-target": "#formfields",
                "hx-vals": '{"type_swap": true}',
            }
        ),
    )

    class Meta:
        model = StorageAccount
        fields = ("type",)

    def __init__(self, *args, **kwargs):
        super(StorageAccountBaseAdminModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["type"].disabled = True

            self.initiate_form_args()

    @staticmethod
    @abstractmethod
    def args_fields() -> Iterable[tuple[str, str]]:
        """
        (
            (form_args_key, model_args_key),
            ...
        )
        """
        raise NotImplementedError

    def get_instance_args(self):
        """
        returns args in a format that the model instance knows about
        """
        return {
            to_key: self.cleaned_data[from_key]
            for from_key, to_key in self.args_fields()
        }

    def initiate_form_args(self):
        """
        populates the initial form data for args fields
        """
        for to_key, from_key in self.args_fields():
            self.fields[to_key].initial = self.instance.args[from_key]

    def clean(self):
        cleaned_data = super(StorageAccountBaseAdminModelForm, self).clean()
        # doing it for the actual StorageForms not this Mixin
        if type(self) != StorageAccountBaseAdminModelForm:
            args = self.instance.validate_schema(
                storage=self.get_selected_storage_class(), args=self.get_instance_args()
            )
            # there is no need to do it again in model.save()
            self.instance.validate_schema_before_saving = False
            self.instance.args = args
            # check if we can write to storage
            storage: Storage = construct_instance(
                self, self.instance, self._meta.fields, self._meta.exclude
            ).get_storage()
            try:
                storage.save(
                    name="test.txt", content=File(ContentFile(b"This is test"))
                )
            except Exception as e:
                code = type(e).__name__
                raise ValidationError(f"{code}: {str(e)}", code=code)
        return cleaned_data

    def get_selected_storage_class(self):
        """
        returns the storage type that is selected
        """
        return get_storage_by_identity(self.cleaned_data["type"])


class MinioSAAdminModelForm(StorageAccountBaseAdminModelForm):
    key = forms.CharField(max_length=255)
    secret = forms.CharField(max_length=255)
    host = forms.CharField(max_length=255)
    port = forms.CharField(max_length=5, min_length=2, validators=[integer_validator])
    secure = forms.BooleanField(required=False, initial=True)
    bucket = forms.CharField(max_length=63, min_length=3)
    auto_create_bucket = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(MinioSAAdminModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["host"].disabled = True
            self.fields["port"].disabled = True

    @staticmethod
    def args_fields() -> Iterable[tuple[str, str]]:
        return (
            ("key", "key"),
            ("secret", "secret"),
            ("host", "host"),
            ("port", "port"),
            ("secure", "secure"),
            ("bucket", "bucket"),
            ("auto_create_bucket", "auto_create_container"),
        )


class Minio2SAAdminModelForm(StorageAccountBaseAdminModelForm):
    key = forms.CharField(max_length=255)
    secret = forms.CharField(max_length=255)
    host = forms.CharField(max_length=255)
    port = forms.CharField(max_length=5, min_length=2, validators=[integer_validator])
    secure = forms.BooleanField(required=False, initial=True)
    bucket = forms.CharField(max_length=63, min_length=3)
    auto_create_bucket = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(Minio2SAAdminModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["host"].disabled = True
            self.fields["port"].disabled = True

    @staticmethod
    def args_fields() -> Iterable[tuple[str, str]]:
        return (
            ("key", "key"),
            ("secret", "secret"),
            ("host", "host"),
            ("port", "port"),
            ("secure", "secure"),
            ("bucket", "bucket"),
            ("auto_create_bucket", "auto_create_container"),
        )


def get_base_sa_edit_handler():
    panels = [
        FieldPanel("type"),
    ]

    return ObjectList(panels, base_form_class=StorageAccountBaseAdminModelForm)


def get_minio_sa_edit_handler() -> ObjectList:
    panels = [
        FieldPanel("type"),
        FieldPanel("title"),
        FieldPanel(
            "key",
        ),
        FieldPanel("secret"),
        FieldPanel("host"),
        FieldPanel("port"),
        FieldPanel("secure"),
        FieldPanel("bucket"),
        FieldPanel("auto_create_bucket"),
    ]

    return ObjectList(panels, base_form_class=MinioSAAdminModelForm)


def get_minio2_sa_edit_handler() -> ObjectList:
    panels = [
        FieldPanel("type"),
        FieldPanel("title"),
        FieldPanel(
            "key",
        ),
        FieldPanel("secret"),
        FieldPanel("host"),
        FieldPanel("port"),
        FieldPanel("secure"),
        FieldPanel("bucket"),
        FieldPanel("auto_create_bucket"),
    ]

    return ObjectList(panels, base_form_class=Minio2SAAdminModelForm)


def get_create_storage_account_edit_handler(data: Mapping[str, Any]) -> ObjectList:
    base_storage_form = StorageAccountBaseAdminModelForm(data=data)
    if not base_storage_form.is_valid():
        return get_base_sa_edit_handler()
    storage_class = base_storage_form.get_selected_storage_class()
    if storage_class == MinioAccountStorage:
        return get_minio_sa_edit_handler()
    elif storage_class == Minio2AccountStorage:
        return get_minio2_sa_edit_handler()
    else:
        raise ImproperlyConfigured


def get_edit_storage_account_edit_handler(instance: StorageAccount) -> ObjectList:
    storage_class = instance.get_storage_class()
    if storage_class == MinioAccountStorage:
        return get_minio_sa_edit_handler()
    elif storage_class == Minio2AccountStorage:
        return get_minio2_sa_edit_handler()
    else:
        raise ImproperlyConfigured
