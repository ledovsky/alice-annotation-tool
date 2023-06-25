from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination

from data_app.models import Dataset
from .models import BackgroundTask
from .serializers import RunBackgroundTaskSerializer, BackgroundTaskSerializer
from .tasks import update_ic_plots, update_links


class RunDatasetBackgroundTaskView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request: HttpRequest):
        serializer = RunBackgroundTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dataset_short_name = Dataset.objects.get(id=serializer.data['dataset_id']).short_name
        if serializer.data['task_name'] == 'update-ic-plots':
            update_ic_plots.delay(dataset_short_name)
        elif serializer.data['task_name'] == 'update-links':
            update_links.delay(dataset_short_name)
        return Response({'status': 'ok'})


class BackgroundTaskView(ListAPIView):
    queryset = BackgroundTask.objects.all().order_by('-created')[:100]
    serializer_class = BackgroundTaskSerializer
    pagination_class = LimitOffsetPagination