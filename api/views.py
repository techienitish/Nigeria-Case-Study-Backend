from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters

from .models import *
from .serializers import *


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    filterset_fields = ['accounts', 'category']
    search_fields = ['name', 'description']
    pagination_class = PageNumberPagination


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['case', 'serverJobId', 'status',
                        'category', 'eventStartDate', 'eventEndDate']


class CallDetailRecordViewSet(viewsets.ModelViewSet):
    queryset = CallDetailRecord.objects.all()
    serializer_class = CallDetailRecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['job', ]
    pagination_class = PageNumberPagination
