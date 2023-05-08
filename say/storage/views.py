from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.views import CreateView, EditView

from .forms import (
    get_create_storage_account_edit_handler,
    get_edit_storage_account_edit_handler,
)
from .models import StorageAccount


class StorageAccountCreateView(CreateView):
    def get_initial(self):
        initial = super(StorageAccountCreateView, self).get_initial()
        if self.request.GET.get("type_swap"):
            initial.update({"type": self.request.GET["type"]})
        return initial

    def get_template_names(self):
        if self.request.htmx:
            return "storage/modeladmin/storageaccount/htmx/create_formfields.html"
        return super(StorageAccountCreateView, self).get_template_names()

    def get_edit_handler(self):
        edit_handler = get_create_storage_account_edit_handler(
            self.request.GET or self.request.POST
        )
        return edit_handler.bind_to_model(self.model_admin.model)


class StorageAccountEditView(EditView):
    def get_edit_handler(self):
        edit_handler = get_edit_storage_account_edit_handler(self.instance)
        return edit_handler.bind_to_model(self.model_admin.model)


class StorageAccountAdmin(ModelAdmin):
    model = StorageAccount
    base_url_path = "storageaccount"
    menu_label = "StorageAccount"
    add_to_settings_menu = True
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title",)

    create_view_class = StorageAccountCreateView
    create_template_name = "storage/modeladmin/storageaccount/create.html"
    edit_view_class = StorageAccountEditView

    def get_edit_handler(self, instance=None, request=None):
        # to make sure all edit handlers are defined explicitly in view classes
        raise ValueError("Make sure using view specific edit handler")
