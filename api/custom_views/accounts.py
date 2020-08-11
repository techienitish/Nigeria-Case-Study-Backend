import json
from django.core import serializers
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from rest_framework.response import Response

from ..models import Account, Department, Case, Group
from ..serializers import AccountSerializer


class AccountsList(APIView):

    def get(self, request, format='json'):
        accounts = Account.objects.all().values()
        for account in accounts:
            user = User.objects.filter(id=account['user_id']).values().first()
            department = Department.objects.filter(
                id=account['department_id']).values().first()
            cases = Case.objects.filter(accounts__in=[account['id']]).exclude(
                name='DEFAULT_CASE_CHECK_OT').values()
            account['cases'] = cases
            account['department'] = department
            account['first_name'] = user['first_name']
            account['last_name'] = user['last_name']
            account['email'] = user['email']
            account['username'] = user['username']
            del account['user_id']
            del account['department_id']

        return Response(accounts)

    def post(self, request, format='json'):
        username = request.data['username']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        phone = request.data['phone']
        group_id = request.data['group']
        password = request.data['password']
        disabled = request.data['disabled']
        designation = request.data['designation']
        department_id = request.data['department']
        startDate = request.data['start_date']
        endDate = request.data['end_date']

        group = Group.objects.get(pk=group_id)

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.save()

        account = Account.objects.create(
            user=user,
            phone=phone,
            group=group,
            disabled=disabled,
            designation=designation,
            department=Department.objects.get(pk=department_id),
            startDate=startDate,
            endDate=endDate
        )

        customResponse = {
            'id': account.id,
            'first_name': account.user.first_name,
            'last_name': account.user.last_name,
            'email': account.user.email,
            'group': Group.objects.filter(id=group_id).values().first(),
            'username': account.user.username,
            'start_date': account.startDate,
            'end_date': account.endDate,
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
        username = request.data['username']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        phone = request.data['phone']
        group_id = request.data['group']
        disabled = request.data['disabled']
        designation = request.data['designation']
        department_id = request.data['department']
        startDate = request.data['start_date']
        endDate = request.data['end_date']

        user = User.objects.get(pk=account.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        account.user = user
        account.phone = phone
        account.group = Group.objects.get(pk=group_id)
        account.disabled = disabled
        account.startDate = startDate
        account.endDate = endDate
        account.designation = designation
        account.department = Department.objects.get(pk=department_id)
        account.save()

        customResponse = {
            'id': account.id,
            'first_name': account.user.first_name,
            'last_name': account.user.last_name,
            'email': account.user.email,
            'group': Group.objects.filter(id=group_id).values().first(),
            'username': account.user.username,
            'start_date': account.startDate,
            'end_date': account.endDate,
            'disabled': account.disabled,
            'department': Department.objects.filter(id=account.department.id).values().first(),
            'designation': account.designation
        }

        return Response(customResponse, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        account = Account.objects.get(pk=pk)
        account.user.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
