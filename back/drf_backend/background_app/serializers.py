from rest_framework import serializers

from .models import BackgroundTask


class RunDatasetBackgroundTaskSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField()
    task_name = serializers.ChoiceField(
        choices=['update-ic-plots', 'update-links', 'update-download-item']
    )


class RunBackgroundTaskSerializer(serializers.Serializer):
    task_name = serializers.ChoiceField(
        choices=['update-dataset-stats']
    )


class BackgroundTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundTask
        fields = '__all__'