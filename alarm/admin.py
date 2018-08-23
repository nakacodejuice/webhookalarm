from django.contrib import admin
from alarm.models import *
admin.site.register([Request, Alarms,users])