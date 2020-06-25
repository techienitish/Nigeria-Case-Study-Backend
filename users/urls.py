from django.urls import path, include
from rest_framework.authtoken import views

from .views import UserView, LogoutView

urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('users/', UserView.as_view()),
]
