from rest_framework.generics import ListAPIView

from .serializers import DatasetDownloadItemSerializer
from .models import DatasetDownloadItem

## Downloads

class DatasetDownloadActual(ListAPIView):
    serializer_class = DatasetDownloadItemSerializer
    queryset = DatasetDownloadItem.objects.filter(is_actual=True)
