from django.contrib import admin

from .models import TelegramInstance


@admin.register(TelegramInstance)
class TelegramInstanceWAdmin(admin.ModelAdmin):
    pass
