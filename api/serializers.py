from rest_framework import serializers

from .models import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class HandsetHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HandsetHistory
        fields = '__all__'

class CallDetailRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallDetailRecord
        fields = '__all__'
