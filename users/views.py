from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer

group_parameter = openapi.Parameter(
    'group',
    openapi.IN_QUERY,
    description='analysts, supervisors, admins',
    type=openapi.TYPE_STRING
)
token_parameter = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='Token <TOKEN>',
    type=openapi.TYPE_STRING
)


class LogoutView(APIView):

    @swagger_auto_schema(
        operation_description="Create new user",
        manual_parameters=[token_parameter],
        responses={
            400: 'Invalid token',
            200: 'Logged out successfully'
        }
    )
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):

    @swagger_auto_schema(
        operation_description="Create new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'group'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Email of new user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of new user'),
                'group': openapi.Schema(type=openapi.TYPE_STRING, description='Group that new user belongs to, options are: analysts, supervisors or admins')
            },
        ),
        responses={
            400: 'Missing group/username/password key',
            201: UserSerializer
        }
    )
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        try:
            user_group = request.data['group']
            group = Group.objects.get(name=user_group)
            if serializer.is_valid() and group != None:
                user = serializer.save()
                if user:
                    user.is_staff = True
                    user.groups.add(group)
                    token = Token.objects.create(user=user)
                    response_data = serializer.data
                    response_data['token'] = token.key
                    del response_data['password']
                    return Response(response_data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'error': 'Group does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Get users",
        manual_parameters=[group_parameter],
        responses={
            400: 'User not found',
            200: UserSerializer(many=True)
        }
    )
    def get(self, request, format='json'):
        group_filter = request.query_params.get('group', None)
        if group_filter:
            users = User.objects.filter(groups__name__in=[group_filter])
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        if serializer:
            response_data = serializer.data
            for user in response_data:
                del user['password']
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
