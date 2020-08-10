from django.contrib import admin
from .models import *

admin.site.register([Account, Department, Case, Job,
                     HandsetHistory, CallDetailRecord])
