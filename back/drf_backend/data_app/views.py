from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import ICACreateSerializer, UserAnnotationSerializer
from .models import Dataset, ICAComponent, Annotation


#
### ICA
#

class ICACreateView(APIView):
    serializer_class = ICACreateSerializer
    queryset = ICAComponent.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ICACreateSerializer(data=request.data)
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user

        if serializer.is_valid():
            serializer.save(uploaded_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
### Dataset operations
#

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


class ResetDatasetView(DatasetOperationsBaseView):
    def do_work(self, dataset):
        if dataset.locked:
            raise ValidationError(f'dataset {dataset.short_name} is locked')
        ics = ICAComponent.objects.filter(dataset=dataset).delete()


class LockDatasetView(DatasetOperationsBaseView):
    def do_work(self, dataset):
        dataset.locked = True
        dataset.save()


class UnlockDatasetView(DatasetOperationsBaseView):
    def do_work(self, dataset):
        dataset.locked = False
        dataset.save()


class TestLongRequestView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        import time
        for i in range(8):
            time.sleep(10)
        return Response({'status': 'ok'})

#
### Annotations
#

class UserAnnotationByIcView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAnnotationSerializer

    def get(self, request, ic_id):
        try:
            obj = Annotation.objects.get(ic=ic_id, user=request.user)
            serializer = self.serializer_class(obj)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({})

    def post(self, request, ic_id):
        create = False
        data = request.data
        data['ic'] = ic_id
        context = {
            'request': self.request,
        }
        try:
            obj = Annotation.objects.get(ic=ic_id, user=request.user)
            serializer = self.serializer_class(obj, data=data, context=context)
        except ObjectDoesNotExist:
            serializer = self.serializer_class(data=data, context=context)
            create = True

        serializer.is_valid(raise_exception=True)
        serializer.save()
        if create:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data)

