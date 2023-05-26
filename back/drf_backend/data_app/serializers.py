import json

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Dataset, Subject, ICAComponent, ICAData, Annotation


class ICADataSerializer(serializers.Serializer):
    ica_data = serializers.JSONField()
    ica_weights = serializers.JSONField()


class ICACreateSerializer(serializers.ModelSerializer):

    dataset = serializers.SlugRelatedField(
        many=False,
        slug_field='short_name',
        queryset=Dataset.objects.all()
    )

    data_obj = ICADataSerializer()
    subject = serializers.CharField(max_length=128)

    class Meta:
        model = ICAComponent
        fields = ('id',
                  'name',
                  'subject',
                  'dataset',
                  'sfreq',
                  'data_obj'
                  )

    def to_internal_value(self, data):
        data['data_obj'] = data.pop('data')
        return super().to_internal_value(data)

    def create(self, validated_data):
        ica_data = validated_data.pop('data_obj')
        ica_data['ica_weights'] = json.dumps(ica_data['ica_weights'])
        ica_data['ica_data'] = json.dumps(ica_data['ica_data'])
        ica_data_obj = ICAData.objects.create(**ica_data)
        subject_name = validated_data.pop('subject')
        try:
            subject = Subject.objects.get(dataset=validated_data['dataset'], name=subject_name)
        except ObjectDoesNotExist:
            subject = Subject.objects.create(dataset=validated_data['dataset'], name=subject_name)
        ic = ICAComponent.objects.create(data_obj=ica_data_obj, subject_name=subject_name, subject=subject, **validated_data)
        return ic


class UserAnnotationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Annotation
        fields = '__all__'


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'short_name', 'full_name', 'description', 'annotation_version')
