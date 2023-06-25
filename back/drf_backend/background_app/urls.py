from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    RunDatasetBackgroundTaskView, 
    RunBackgroundTaskView,
    BackgroundTaskView
)


urlpatterns = [
    path('background/run-dataset', RunDatasetBackgroundTaskView.as_view(), name='background-run-dataset'),
    path('background/run', RunBackgroundTaskView.as_view(), name='background-run'),
    path('background/list', BackgroundTaskView.as_view(), name='background-list'),
]


urlpatterns = format_suffix_patterns(urlpatterns)