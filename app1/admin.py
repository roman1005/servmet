from django.contrib import admin
from app1.models import Service_CI, Staff
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Service_CI, SimpleHistoryAdmin)
admin.site.register(Staff, SimpleHistoryAdmin)
# Register your models here.
