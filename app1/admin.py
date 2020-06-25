from django.contrib import admin
from django.contrib.admin.templatetags.admin_modify import submit_row
from app1.models import Service, Staff, Metric, MetricMeasurement, MetricValue
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import redirect
from django.contrib.admin.templatetags import admin_modify
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.signals import user_logged_in


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='Public'))
    try:
        staff_id = Staff.objects.get(name = instance.first_name+" "+instance.last_name)
        if Service.objects.filter(owner=staff_id).count() > 0:
            instance.groups.add(Group.objects.get(name='ServiceMetricOwner'))
    except:
        pass

@receiver(pre_save, sender=User)
def set_new_user_staff(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.is_staff = True

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    try:
        staff_id = Staff.objects.get(name = user.first_name+" "+user.last_name)
        if Service.objects.filter(owner=staff_id).count() > 0:
            user.groups.add(Group.objects.get(name='ServiceMetricOwner'))
        else:
            user.groups.remove(Group.objects.get(name='ServiceMetricOwner'))
    except:
        if Group.objects.get(name='ServiceMetricOwner') in user.groups.all():
            user.groups.remove(Group.objects.get(name='ServiceMetricOwner'))

class RemoveButtons:

    submit_row = admin_modify.submit_row

    def submit_row_custom(context):
        ctx = submit_row(context)
        ctx['show_save_and_add_another'] = False
        ctx['show_save_and_continue'] = False
        return ctx

    admin_modify.submit_row = submit_row_custom

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
    template = "admin/edit_inline/services.html"


class MetricInline(LinkedInline):
    model = Metric
    extra = 0
    fields = ["metric_name"]
    readonly_fields = ["metric_name"]
    ordering = ('metric_order',)
    max_num = 0


class MetricValueInline(admin.TabularInline):
    template = "admin/edit_inline/metrics.html/"
    model = MetricValue
    extra = 0
    per_page = 12
    ordering = ('-date_begin',)
    #readonly_fields = ['metric', 'value', 'date_begin', 'date_end']

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


class ServiceAdmin(SimpleHistoryAdmin, admin.ModelAdmin, RemoveButtons):
    change_form_template = "admin/edit_inline/change_form.html/"
    inlines = [
        MetricInline,
    ]
    search_fields = ('service_name', 'design_id', 'owner__name')
    ordering = ('totalorder',)
    exclude = ['totalorder',]

    def response_change(self, request, obj):
        return redirect(request.path)

    def __unicode__(self):
        return self.totalorder


class StaffAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)

    def __unicode__(self):
        return self.name

class MetricAdmin(SimpleHistoryAdmin, admin.ModelAdmin, RemoveButtons):

    change_form_template = "admin/edit_inline/change_form.html/"
    ordering = ('service__totalorder', 'metric_order', )
    search_fields = ('metric_name', 'design_id')
    inlines = [
        MetricValueInline
    ]
    exclude = ['date_begin', 'date_end',]

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:  # editing an existing object
            return self.readonly_fields + ('service', 'design_id', 'metric_name', 'description', 'status', 'metric_order', 'publ_regularity', 'publ_deadline', 'measr_regularity', 'nature')
        return self.readonly_fields

    #readonly_fields = ['service', 'design_id', 'metric_name', 'description', 'status', 'metric_order', 'publ_regularity', 'publ_deadline', 'measr_regularity', 'nature']

    def response_change(self, request, obj):
        return redirect(request.path)
    '''
    def save_model(self, request, obj, form, change):
        return redirect(request.path)
    '''

    '''
    def save_formset(self, request, form, formset, change):

        if len(formset.forms) <= len(formset.initial_forms):
            return formset.save()

        new_forms = self.get_new(formset.initial_forms, formset.forms)
        for form in new_forms:
            answer = self.check_overlapping(form.instance)
            if answer == 0:
                #raise ValidationError('Date begin or date end field overlaps with other metric values.')
                return redirect(request.path)
            elif answer == 1:
                #raise ValidationError(request, 'Date begin cannot be later than date end.')
                return redirect(request.path)

            else:
                return formset.save()

    def get_new(self, initial_forms, forms):

        new_forms = []
        for mval in forms:
            if mval not in initial_forms:
                new_forms.append(mval)
        return new_forms

    def check_overlapping(self, obj):
        metric_value_overlapping_start = MetricValue.objects.filter(date_begin__gte=obj.date_begin,
                                                                    date_begin__lte=obj.date_end).count()

        # get number of items that have an overlapping end date
        metric_value_overlapping_end = MetricValue.objects.filter(date_end__gte=obj.date_begin,
                                                                  date_end__lte=obj.date_end).count()

        overlapping_metric_value_present = metric_value_overlapping_start > 0 or metric_value_overlapping_end > 0

        if overlapping_metric_value_present:
            # print("Trying to overlap metric value")
            return 0 #ValidationError('Date begin or date end field overlaps with other metric values.')
        elif obj.date_begin > obj.date_end:
            return 1 #ValidationError('Date begin cannot be later than date end.')
        else:
            return 2
        '''


class MetricValueAdmin(SimpleHistoryAdmin, admin.ModelAdmin, RemoveButtons):

    change_form_template = "admin/edit_inline/metric_values.html/"

    def response_change(self, request, obj):
        return redirect(request.path)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        return redirect(request.path)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Metric, MetricAdmin)
admin.site.register(MetricMeasurement, SimpleHistoryAdmin)
admin.site.register(MetricValue, MetricValueAdmin)

# Register your models here.
