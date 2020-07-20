from django.contrib import admin
from .models import *

admin.site.register([Account, Department, Head, Case, Job, CallDetailRecord])
