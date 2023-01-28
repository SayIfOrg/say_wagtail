from abc import abstractmethod
from typing import Mapping, Any, Iterable

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import integer_validator
from django.utils.translation import gettext as _
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin.panels import ObjectList, FieldPanel

from .storage import get_storage_by_identity, MinioStorage, Minio2Storage
from .models import StorageAccount, AVAILABLE_STORAGES


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

            self.fill_form_args()

    @staticmethod
    @abstractmethod
    def args_fields() -> Iterable[str]:
        raise NotImplementedError

    def fill_instant_args(self):
        self.instance.args = {
            field: self.cleaned_data[field] for field in self.args_fields()
        }

    def fill_form_args(self):
        for field_name in self.args_fields():
            self.fields[field_name].initial = self.instance.args[field_name]

    def save(self, commit=True):
        self.fill_instant_args()
        return super(StorageAccountBaseAdminModelForm, self).save(commit)

    def get_selected_storage_class(self):
        return get_storage_by_identity(self.cleaned_data["type"])


class MinioSAAdminModelForm(StorageAccountBaseAdminModelForm):
    key = forms.CharField(max_length=255)
    secret = forms.CharField(max_length=255)
    host = forms.CharField(max_length=255)
    port = forms.CharField(max_length=5, min_length=2, validators=[integer_validator])
    secure = forms.BooleanField(required=False, initial=True)
    bucket = forms.CharField(max_length=63)
    auto_create_container = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(MinioSAAdminModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["host"].disabled = True
            self.fields["port"].disabled = True

    @staticmethod
    def args_fields() -> Iterable[str]:
        return (
            "key",
            "secret",
            "host",
            "port",
            "secure",
            "bucket",
            "auto_create_container",
        )


class Minio2SAAdminModelForm(StorageAccountBaseAdminModelForm):
    key = forms.CharField(max_length=255)
    secret = forms.CharField(max_length=255)
    host = forms.CharField(max_length=255)
    port = forms.CharField(max_length=5, min_length=2, validators=[integer_validator])
    secure = forms.BooleanField(required=False, initial=True)
    bucket = forms.CharField(max_length=63)
    auto_create_container = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(Minio2SAAdminModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["host"].disabled = True
            self.fields["port"].disabled = True

    @staticmethod
    def args_fields() -> Iterable[str]:
        return (
            "key",
            "secret",
            "host",
            "port",
            "secure",
            "bucket",
            "auto_create_container",
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
        FieldPanel("auto_create_container"),
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
        FieldPanel("auto_create_container"),
    ]

    return ObjectList(panels, base_form_class=Minio2SAAdminModelForm)


def get_create_storage_account_edit_handler(data: Mapping[str, Any]) -> ObjectList:
    base_storage_form = StorageAccountBaseAdminModelForm(data=data)
    if not base_storage_form.is_valid():
        return get_base_sa_edit_handler()
    storage_class = base_storage_form.get_selected_storage_class()
    if storage_class == MinioStorage:
        return get_minio_sa_edit_handler()
    elif storage_class == Minio2Storage:
        return get_minio2_sa_edit_handler()
    else:
        raise ImproperlyConfigured


def get_edit_storage_account_edit_handler(instance: StorageAccount) -> ObjectList:
    storage_class = instance.get_storage_class()
    if storage_class == MinioStorage:
        return get_minio_sa_edit_handler()
    elif storage_class == Minio2Storage:
        return get_minio2_sa_edit_handler()
    else:
        raise ImproperlyConfigured
