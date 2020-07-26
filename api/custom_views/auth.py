from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from ..models import Account, Department
from ..serializers import AccountSerializer

class CustomAuth(APIView):

    def post(self, request, format='json'):
        operation = request.data['operation']
        if operation == 'logout':
            try:
                request.user.auth_token.delete()
                return Response({ 'success': True }, status=status.HTTP_200_OK)
            except Exception as ex:
                return Response({ 'error': ex }, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({ 'error': 'Invalid username/password' }, status=status.HTTP_400_BAD_REQUEST)
        else:
            account = Account.objects.filter(user=user).values().first()
            department = Department.objects.filter(id=account['department_id']).values().first()
            account['department'] = department
            account['name'] = user.first_name
            account['username'] = user.get_username()
            token, created = Token.objects.get_or_create(user=user)
            account['token'] = token.key

            del account['user_id']
            del account['department_id']
            
            return Response(account, status=status.HTTP_200_OK)