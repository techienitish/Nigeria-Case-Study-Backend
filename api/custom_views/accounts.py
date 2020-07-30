import json
from django.core import serializers
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from rest_framework.response import Response

from ..models import Account, Department, Case
from ..serializers import AccountSerializer


class AccountsList(APIView):

    def get(self, request, format='json'):
        accounts = Account.objects.all().values()
        for account in accounts:
            user = User.objects.filter(id=account['user_id']).values().first()
            department = Department.objects.filter(
                id=account['department_id']).values().first()
            cases = Case.objects.filter(accounts__in=[account['id']]).exclude(name='DEFAULT_CASE_CHECK_OT').values()
            account['cases'] = cases
            account['department'] = department
            account['name'] = user['first_name']
            account['username'] = user['username']
            del account['user_id']
            del account['department_id']

        return Response(accounts)

    def post(self, request, format='json'):
        name = request.data['name']
        username = request.data['username']
        password = request.data['password']
        designation = request.data['designation']
        department_id = request.data['department']

        user = User.objects.create(
            username=username,
            first_name=name
        )
        user.set_password(password)
        user.save()

        account = Account.objects.create(
            user=user,
            designation=designation,
            department=Department.objects.get(pk=department_id),
        )

        customResponse = {
            'id': account.id,
            'name': account.user.first_name,
            'username': account.user.username,
            'disabled': account.disabled,
            'department': Department.objects.filter(id=account.department.id).values().first(),
            'designation': account.designation
        }

        return Response(customResponse, status=status.HTTP_201_CREATED)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def put(self, request, pk):
        account = Account.objects.get(pk=pk)
        name = request.data['name']
        username = request.data['username']
        disabled = request.data['disabled']
        designation = request.data['designation']
        department_id = request.data['department']

        user = User.objects.get(pk=account.user.id)
        user.first_name = name
        user.username = username
        user.save()

        account.user = user
        account.disabled = disabled
        account.designation = designation
        account.department = Department.objects.get(pk=department_id)
        account.save()

        customResponse = {
            'id': account.id,
            'name': account.user.first_name,
            'username': account.user.username,
            'disabled': account.disabled,
            'department': Department.objects.filter(id=account.department.id).values().first(),
            'designation': account.designation
        }

        return Response(customResponse, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        account = Account.objects.get(pk=pk)
        account.user.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
