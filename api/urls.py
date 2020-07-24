from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('cases', CaseViewSet)
router.register('jobs', JobViewSet)
router.register('cdr', CallDetailRecordViewSet)

urlpatterns = [
    path('api/departments/', ListDepartments.as_view()),
    path('api/', include(router.urls)),
]
