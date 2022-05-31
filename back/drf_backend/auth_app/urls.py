from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from auth_app import views
# from rest_framework.authtoken import views

urlpatterns = [
    path('auth', views.CustomAuthToken.as_view(), name='auth'),
    path('browsable-api-auth/', include('rest_framework.urls')),
]
#
urlpatterns = format_suffix_patterns(urlpatterns)
