from django.urls import path, include
from rest_framework import routers

from .views import *
from .custom_views.auth import *
from .custom_views.departments import *
from .custom_views.accounts import *
from .custom_views.cdr_columns import *

router = routers.DefaultRouter()
router.register('cases', CaseViewSet)
router.register('jobs', JobViewSet)
router.register('cdr', CallDetailRecordViewSet)

urlpatterns = [
    # Auth
    path('api/auth/', CustomAuth.as_view()),
    # Accounts
    path('api/accounts/', AccountsList.as_view()),
    path('api/accounts/<int:pk>/', AccountDetail.as_view()),
    # Departments
    path('api/departments/', DepartmentList.as_view()),
    path('api/departments/<int:pk>/', DepartmentDetail.as_view()),
    # CallDetailRecord columns
    path('api/cdr/columns/', CdrColumns.as_view()),
    # General CRUD
    path('api/', include(router.urls)),
]
