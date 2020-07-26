from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from ..models import Account, Department
from ..serializers import AccountSerializer

class CustomAuth(APIView):

    def post(self, request, format='json'):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({ 'error': 'Invalid username/password' }, status=status.HTTP_400_BAD_REQUEST)
        else:
            account = Account.objects.filter(user=user).values().first()
            return Response(account)