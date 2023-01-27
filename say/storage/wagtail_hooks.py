from wagtail.contrib.modeladmin.options import modeladmin_register

from .views import StorageAccountAdmin


modeladmin_register(StorageAccountAdmin)
