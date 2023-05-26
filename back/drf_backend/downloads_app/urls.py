from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from downloads_app import views

urlpatterns = [
    path('downloads/actual', views.DatasetDownloadActual.as_view(), name='downloads-actual'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
