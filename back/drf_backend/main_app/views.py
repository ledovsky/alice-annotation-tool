from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend


from data_app.views import DatasetOperationsBaseView
from .serializers import ICAListSerializer, ICADetailedSerializer, DatasetDetailedSerializer, AnnotationListSerializer
from .models import ICAComponent, Dataset, Annotation, ICAImages, ICALinks


class APIRootView(APIView):
    def get(self, request):
        data = {

            ### auth_app
            'auth': reverse('auth', request=request),

            ### data_app
            'data-ic': reverse('data-ic', request=request),
            'data-dataset-reset': reverse('data-dataset-reset', request=request, args=[1]),
            'data-dataset-lock': reverse('data-dataset-lock', request=request, args=[1]),
            'data-dataset-unlock': reverse('data-dataset-unlock', request=request, args=[1]),
            'data-user-annotation-by-ic': reverse('data-user-annotation-by-ic', request=request, args=[1]),
            'downloads-actual': reverse('downloads-actual', request=request),

            ## main_app
            'view-ic-list': reverse('view-ic-list', request=request),
            'view-ic': reverse('view-ic', request=request, args=[1]),
            'view-annotations-list': reverse('view-annotations-list', request=request),
            'view-datasets-list': reverse('view-datasets-list', request=request),
            'view-datasets-retrieve': reverse('view-datasets-retrieve', request=request, args=[1]),
            'view-datasets-recalc': reverse('view-datasets-recalc', request=request, args=[1]),
        }
        return Response(data)


class ICAListView(generics.ListAPIView):
    serializer_class = ICAListSerializer
    queryset = ICAComponent.objects.all().order_by('subject_name', 'name')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['dataset']
    search_fields = ['name', 'subject']
    permission_classes = [IsAuthenticated]


class ICADetailedView(generics.RetrieveAPIView):
    serializer_class = ICADetailedSerializer
    queryset = ICAComponent.objects.all()
    permission_classes = [IsAuthenticated]


class DatasetListView(generics.ListAPIView):
    serializer_class = DatasetDetailedSerializer
    queryset = Dataset.objects.all()
    permission_classes = [IsAuthenticated]


class DatasetRetrieveView(generics.RetrieveAPIView):
    serializer_class = DatasetDetailedSerializer
    queryset = Dataset.objects.all()
    permission_classes = [IsAuthenticated]


class DatasetOperationsBaseView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        dataset = self.get_object(pk)
        self.do_work(dataset)
        return Response({'status': 'ok'})

    def do_work(self, dataset):
        raise NotImplementedError


class DatasetRecalcView(DatasetOperationsBaseView):
    def do_work(self, dataset):
        ICAImages.update_images(dataset.short_name)
        ICALinks.update_links(dataset.short_name)


class AnnotationListView(generics.ListCreateAPIView):
    serializer_class = AnnotationListSerializer
    queryset = Annotation.objects.all()
    filterset_fields = ['ic_id']
    permission_classes = [IsAuthenticated]
