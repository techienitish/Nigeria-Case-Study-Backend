from django.contrib import admin
from .models import *

admin.site.register([Account, Department, Group, Zone, Poi, Case, Job,
                     HandsetHistory, CallDetailRecord])
