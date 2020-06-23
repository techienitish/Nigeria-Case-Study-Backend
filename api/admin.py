from django.contrib import admin
from .models import *

admin.site.register([Case, Job, CallDetailRecord])
