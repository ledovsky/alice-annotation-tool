from django.contrib import admin

# Register your models here.

from .models import ICAComponent, ICAData, Dataset, Annotation


@admin.register(ICAComponent)
class ICAComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject', 'dataset')


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'ic', 'get_username', 'get_user_fullname')

    def get_username(self, obj):
        return obj.user.username
    get_username.description = 'Username'

    def get_user_fullname(self, obj):
        return obj.user.get_full_name()
    get_user_fullname.description = 'User full name'


admin.site.register(ICAData)
admin.site.register(Dataset)
