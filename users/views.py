from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer


class UserView(APIView):

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        user_group = request.data['group']
        try:
            group = Group.objects.get(name=user_group)
            if serializer.is_valid() and group != None:
                user = serializer.save()
                if user:
                    user.groups.add(group)
                    response_data = serializer.data
                    del response_data['password']
                    return Response(response_data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'error': 'Group does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format='json'):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        if serializer:
            response_data = serializer.data
            for user in response_data:
                del user['password']
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
