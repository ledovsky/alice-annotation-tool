from django.contrib import admin

# Register your models here.

from .models import DatasetStats, ICAImages, ICALinks

admin.site.register(DatasetStats)
admin.site.register(ICAImages)
admin.site.register(ICALinks)
