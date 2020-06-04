from django.contrib import admin
from app1.models import Service, Staff, Metric, MetricMeasurement, MetricValue
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator


class InlineChangeList(object):
    can_show_all = True
    multi_page = True
    get_query_string = ChangeList.__dict__['get_query_string']

    def __init__(self, request, page_num, paginator):
        self.show_all = 'all' in request.GET
        self.page_num = page_num
        self.paginator = paginator
        self.result_count = paginator.count
        self.params = dict(request.GET.items())


class LinkedInline(admin.options.InlineModelAdmin):
    template = "admin/edit_inline/stacked.html"


class MetricInline(LinkedInline):
    model = Metric
    extra = 0
    fields = ["metric_name"]
    ordering = ('metric_order',)
    per_page = 2

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(MetricInline, self).get_formset(
            request, obj, **kwargs)

        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)

                qs = self.queryset
                paginator = Paginator(qs, self.per_page)
                try:
                    page_num = int(request.GET.get('page', ['0'])[0])
                except ValueError:
                    page_num = 0

                try:
                    page = paginator.page(page_num + 1)
                except (EmptyPage, InvalidPage):
                    page = paginator.page(paginator.num_pages)

                self.page = page
                self.cl = InlineChangeList(request, page_num, paginator)
                self.paginator = paginator

                if self.cl.show_all:
                    self._queryset = qs
                else:
                    self._queryset = page.object_list

        PaginationFormSet.per_page = self.per_page
        return PaginationFormSet


class MetricValueInline(LinkedInline):

    template = 'admin/edit_inline/inline_metrics.html'
    template = "admin/edit_inline/stacked.html"
    model = MetricValue
    extra = 0
    per_page = 10
    ordering = ('-date_begin',)

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(MetricValueInline, self).get_formset(
            request, obj, **kwargs)

        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)

                qs = self.queryset
                paginator = Paginator(qs, self.per_page)
                try:
                    page_num = int(request.GET.get('page', ['0'])[0])
                except ValueError:
                    page_num = 0

                try:
                    page = paginator.page(page_num + 1)
                except (EmptyPage, InvalidPage):
                    page = paginator.page(paginator.num_pages)

                self.page = page
                self.cl = InlineChangeList(request, page_num, paginator)
                self.paginator = paginator

                if self.cl.show_all:
                    self._queryset = qs
                else:
                    self._queryset = page.object_list

        PaginationFormSet.per_page = self.per_page
        return PaginationFormSet

#class MetricMeasurementInLine()


class ServiceAdmin(admin.ModelAdmin):
    inlines = [
        MetricInline,
    ]
    search_fields = ('service_name', 'design_id', 'owner__name')
    ordering = ('totalorder',)
    exclude = ['totalorder',]

    def __unicode__(self):
        return self.totalorder


class StaffAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)

    def __unicode__(self):
        return self.name

class MetricAdmin(admin.ModelAdmin):
    ordering = ('service__totalorder', 'metric_order', )
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
