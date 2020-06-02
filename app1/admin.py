from django.contrib import admin
from app1.models import Service, Staff, Metric, MetricMeasurement, MetricValue
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator


class LinkedInline(admin.options.InlineModelAdmin):
    template = "admin/edit_inline/tabular_paginator.html"
    admin_model_path = None

    def __init__(self, *args):
        super(LinkedInline, self).__init__(*args)
        if self.admin_model_path is None:
            self.admin_model_path = self.model.__name__.lower()


class MetricInline(LinkedInline):
    model = Metric
    extra = 0
    fields = [ "metric_name"]


class ServiceAdmin(admin.ModelAdmin):
    inlines = [
        MetricInline,
    ]
    search_fields = ('service_name', 'design_id')
    ordering = ('service_name',)

class StaffAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)

admin.site.register(Service, ServiceAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Metric, SimpleHistoryAdmin)
admin.site.register(MetricMeasurement, SimpleHistoryAdmin)
admin.site.register(MetricValue, SimpleHistoryAdmin)
# Register your models here.
