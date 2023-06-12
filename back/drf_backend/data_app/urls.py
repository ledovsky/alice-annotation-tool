from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from data_app import views

urlpatterns = [
    path('ic', views.ICACreateView.as_view(), name='data-ic'),
    path('datasets/lock/<int:pk>', views.LockDatasetView.as_view(), name='data-dataset-lock'),
    path('datasets/unlock/<int:pk>', views.UnlockDatasetView.as_view(), name='data-dataset-unlock'),
    path('datasets/reset/<int:pk>', views.ResetDatasetView.as_view(), name='data-dataset-reset'),
    path('user-annotation-by-ic/<int:ic_id>', views.UserAnnotationByIcView.as_view(), name='data-user-annotation-by-ic'),
    path('test-long-request', views.TestLongRequestView.as_view(), name='data-test-long-request'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
