from rest_framework import serializers

from data_app.serializers import DatasetSerializer
from downloads_app.models import DatasetDownloadItem


class DatasetDownloadItemSerializer(serializers.ModelSerializer):

    dataset = DatasetSerializer()

    class Meta:
        model = DatasetDownloadItem
        fields = '__all__'
