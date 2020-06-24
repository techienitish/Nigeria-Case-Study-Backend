from django.urls import path, include
from rest_framework.authtoken import views

from .views import UserView

urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('users/', UserView.as_view()),
]
