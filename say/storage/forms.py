from abc import abstractmethod

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import integer_validator
from django.http import HttpRequest
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

    @abstractmethod
    def include_args(self):
        raise NotImplementedError

    def save(self, commit=True):
        self.include_args()
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

    def include_args(self):
        self.instance.args = {
            field: self.cleaned_data[field]
            for field in (
                "key",
                "secret",
                "host",
                "port",
                "secure",
                "bucket",
                "auto_create_container",
            )
        }


class Minio2SAAdminModelForm(StorageAccountBaseAdminModelForm):
    key = forms.CharField(max_length=255)
    secret = forms.CharField(max_length=255)
    host = forms.CharField(max_length=255)
    port = forms.CharField(max_length=5, min_length=2, validators=[integer_validator])
    secure = forms.BooleanField(required=False, initial=True)
    bucket = forms.CharField(max_length=63)
    auto_create_container = forms.BooleanField(required=False, initial=True)

    def include_args(self):
        self.instance.args = {
            field: self.cleaned_data[field]
            for field in (
                "key",
                "secret",
                "host",
                "port",
                "secure",
                "bucket",
                "auto_create_container",
            )
        }


def get_base_sa_edit_handler():
    panels = [
        FieldPanel("type"),
    ]

    return ObjectList(panels, base_form_class=StorageAccountBaseAdminModelForm)


def get_minio_sa_edit_handler():
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


def get_minio2_sa_edit_handler():
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


def get_storage_account_edit_handler(request: HttpRequest):
    base_storage_form = StorageAccountBaseAdminModelForm(
        data=(request.GET or request.POST)
    )
    if not base_storage_form.is_valid():
        return get_base_sa_edit_handler()
    storage_class = base_storage_form.get_selected_storage_class()
    if storage_class == MinioStorage:
        return get_minio_sa_edit_handler()
    elif storage_class == Minio2Storage:
        return get_minio2_sa_edit_handler()
    else:
        raise ImproperlyConfigured
