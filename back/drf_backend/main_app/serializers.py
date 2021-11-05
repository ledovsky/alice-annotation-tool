from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import serializers

from auth_app.serializers import UserSerializer
from data_app.models import Dataset, ICAComponent
# from data_app.serializers import AnnotationSerializer
from .models import DatasetStats, Annotation, ICAImages, ICALinks


class ICAListSerializer(serializers.ModelSerializer):

    dataset = serializers.SlugRelatedField(
        many=False,
        slug_field='short_name',
        queryset=Dataset.objects.all()
    )

    is_annotated = serializers.SerializerMethodField()
    annotation = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = ICAComponent
        fields = ('id',
                  'name',
                  'subject',
                  'dataset',
                  'sfreq',
                  'uploaded_by',
                  'uploaded_at',
                  'annotation',
                  'is_annotated')

        read_only_fields = ('uploaded_by', 'uploaded_at', 'is_annotated', 'annotation')
    
    def get_subject(self, obj):
        return obj.subject_name

    def get_is_annotated(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        try:
            Annotation.objects.get(ic=obj.id, user=user)
            return True
        except ObjectDoesNotExist:
            return False

    def get_annotation(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return {}
        try:
            annotation = Annotation.objects.get(ic=obj.id, user=user)
            return AnnotationListSerializer(annotation).data
        except ObjectDoesNotExist:
            return {}


class ICAImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICAImages
        fields = '__all__'


class ICALinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICALinks
        fields = '__all__'


class DatasetStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetStats
        fields = ('dataset', 'n_components', 'agreement')


class DatasetDetailedSerializer(serializers.ModelSerializer):
    stats = DatasetStatsSerializer(read_only=True)
    class Meta:
        model = Dataset
        fields = ('id', 'short_name', 'full_name', 'annotation_version', 'stats')


class ICADetailedSerializer(serializers.ModelSerializer):
    # data_obj = ICADataSerializer()
    images = ICAImagesSerializer()
    links = ICALinksSerializer()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = ICAComponent
        fields = ('id',
                  'name',
                  'subject',
                  'dataset',
                  'sfreq',
                  'images',
                  'links',
                  # 'data_obj',
                  'uploaded_by',
                  'uploaded_at',
                  )

    def get_subject(self, obj):
        return obj.subject_name

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['data'] = data.pop('data_obj')
    #     return data



class AnnotationListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Annotation
        fields = '__all__'
