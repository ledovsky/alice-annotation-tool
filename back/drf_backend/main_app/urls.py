from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from main_app import views

urlpatterns = [
    path('', views.APIRootView.as_view()),
    path('view/annotations/list', views.AnnotationListView.as_view(), name='view-annotations-list'),

    path('view/datasets/list', views.DatasetListView.as_view(), name='view-datasets-list'),
    path('view/subjects/list/by-dataset/<int:dataset_id>', views.SubjectListView.as_view(), name='view-subjects-list-by-dataset'),
    path('view/ic/list/by-subject/<int:subject_id>', views.ICAListBySubjectView.as_view(), name='view-ic-list-by-subject'),

    path('view/datasets/<int:pk>', views.DatasetRetrieveView.as_view(), name='view-datasets-retrieve'),
    path('view/subjects/<int:pk>', views.SubjectRetrieveView.as_view(), name='view-subjects-retrieve'),
    path('view/ic/<int:pk>', views.ICADetailedView.as_view(), name='view-ic-retrieve'),

    path('view/datasets/recalc/<int:pk>', views.DatasetRecalcView.as_view(), name='view-datasets-recalc'),
]

urlpatterns = format_suffix_patterns(urlpatterns)