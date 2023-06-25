import json

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from data_app.models import Dataset, Subject, Annotation, ICAComponent
from .serializers import (
    ICAListSerializer, ICADetailedSerializer, DatasetDetailedSerializer, 
    AnnotationListSerializer, SubjectDetailedSerializer
)
from .vis import plot_components


class ICAListBySubjectView(APIView):
    serializer_class = ICAListSerializer

    def get(self, request, subject_id):
        queryset = (ICAComponent
            .objects
            .all()
            .order_by('subject__name', 'name')
            .filter(subject=subject_id)
        )
        context = {
            'request': request,
        }
        serializer = self.serializer_class(queryset, many=True, context=context)
        return Response(serializer.data)
        

class ICADetailedView(generics.RetrieveAPIView):
    serializer_class = ICADetailedSerializer
    queryset = ICAComponent.objects.all()


class DatasetListView(generics.ListAPIView):
    serializer_class = DatasetDetailedSerializer
    queryset = Dataset.objects.all()


class SubjectListView(APIView):
    serializer_class = SubjectDetailedSerializer

    def get(self, request, dataset_id):
        queryset = (Subject
            .objects
            .all()
            .order_by('name')
            .filter(dataset=dataset_id)
        )
        context = {
            'request': request,
        }
        serializer = self.serializer_class(queryset, many=True, context=context)
        return Response(serializer.data)


class DatasetRetrieveView(generics.RetrieveAPIView):
    serializer_class = DatasetDetailedSerializer
    queryset = Dataset.objects.all()


class SubjectRetrieveView(generics.RetrieveAPIView):
    serializer_class = SubjectDetailedSerializer
    queryset = Subject.objects.all()


class AnnotationListView(generics.ListCreateAPIView):
    serializer_class = AnnotationListSerializer
    queryset = Annotation.objects.all()
    filterset_fields = ['ic_id']
    permission_classes = [IsAuthenticated]


class ComponentsPlotView(APIView):
    """Returns Plotly JSON with components plot"""

    def get(self, request, subject_id):
        subject = Subject.objects.get(id=subject_id)
        ic_names = subject.get_ic_names()
        ica_values, ica_epochs, sfreq = subject.get_components_data(60, 0)
        fig = plot_components(ica_values, ica_epochs, ic_names, sfreq)
        fig_json = json.loads(fig.to_json())
        return Response({
            'figure': fig_json,
            'subject_id': subject_id
        })
