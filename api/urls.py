from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register('cases', CaseViewSet)
router.register('jobs', JobViewSet)
router.register('cdr', CallDetailRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
