from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters

from .models import *
from .serializers import *
from csb_project.pagination import CustomPagination


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['case', ]


class PoiViewSet(viewsets.ModelViewSet):
    queryset = Poi.objects.all()
    serializer_class = PoiSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['case', ]


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    filterset_fields = ['accounts', 'category']
    search_fields = ['name', 'description']


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['case', 'serverJobId', 'status',
                        'category', 'startTime', 'endTime']


class HandsetHistoryViewSet(viewsets.ModelViewSet):
    queryset = HandsetHistory.objects.all()
    serializer_class = HandsetHistorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['job', ]


class CallDetailRecordViewSet(viewsets.ModelViewSet):
    queryset = CallDetailRecord.objects.all()
    serializer_class = CallDetailRecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['job', ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return CallDetailRecord.objects.filter().order_by('id')
