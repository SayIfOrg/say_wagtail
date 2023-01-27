from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.views import CreateView

from .forms import get_storage_account_edit_handler
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
        edit_handler = get_storage_account_edit_handler(self.request)
        return edit_handler.bind_to_model(self.model_admin.model)

    def form_valid(self, form):
        form.instance.site = self.request.user.site_user.site
        return super(StorageAccountCreateView, self).form_valid(form)


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
