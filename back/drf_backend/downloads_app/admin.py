from django.contrib import admin

from .models import DatasetDownloadItem


@admin.register(DatasetDownloadItem)
class DatasetDownloadItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'dataset', 'version')