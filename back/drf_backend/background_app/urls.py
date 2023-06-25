from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import RunDatasetBackgroundTaskView, BackgroundTaskView


urlpatterns = [
    path('background/run-dataset', RunDatasetBackgroundTaskView.as_view(), name='background-run-dataset'),
    path('background/list', BackgroundTaskView.as_view(), name='background-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns)