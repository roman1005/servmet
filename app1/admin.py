from django.contrib import admin
from app1.models import Service, Staff, Metric, MetricMeasurement, MetricValue
from simple_history.admin import SimpleHistoryAdmin


class LinkedInline(admin.options.InlineModelAdmin):
    template = "admin/edit_inline/inline_metrics.html"
    #admin_model_path = None

    '''
    def __init__(self, *args):
        super(LinkedInline, self).__init__(*args)
        if self.admin_model_path is None:
            self.admin_model_path = self.model.__name__.lower()
    '''


class MetricInline(LinkedInline):
    model = Metric
    extra = 0
    fields = ["metric_name"]
    ordering = ('metric_order',)

class MetricValueInline(LinkedInline):
    model = MetricValue
    extra = 0
    fields = ['id']
    readonly_fields = ['id']
    ordering = ('-date_begin',)

#class MetricMeasurementInLine()


class ServiceAdmin(admin.ModelAdmin):
    inlines = [
        MetricInline,
    ]
    search_fields = ('service_name', 'design_id', 'owner__name')
    ordering = ('totalorder',)
    exclude = ['totalorder',]


class StaffAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)

    def __unicode__(self):
        return self.name

class MetricAdmin(admin.ModelAdmin):
    ordering = ('metric_name',)
    search_fields = ('metric_name',)
    inlines = [
        MetricValueInline
    ]
    exclude = ['metric_order', 'date_begin', 'date_end',]

admin.site.register(Service, ServiceAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Metric, MetricAdmin)
admin.site.register(MetricMeasurement, SimpleHistoryAdmin)
admin.site.register(MetricValue, SimpleHistoryAdmin)
# Register your models here.
