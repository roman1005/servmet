from django.contrib import admin
from django.contrib.admin.templatetags.admin_modify import submit_row



from app1.models import *
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
from django.contrib.admin import helpers
from django.core.exceptions import ObjectDoesNotExist






@receiver(pre_save, sender=User)
def set_new_user_staff(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.is_staff = True

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    '''after new User is created it is added into the Public group automatically, and if Staff with such name exists - into the ServiceMetricOwner group'''
    if created:
        instance.groups.add(Group.objects.get(name='Public'))
    try:
        staff_id = Staff.objects.get(name = instance.first_name+" "+instance.last_name)
        if Service.objects.filter(owner=staff_id).count() > 0:
            instance.groups.add(Group.objects.get(name='ServiceMetricOwner'))
    except Staff.DoesNotExist:
        pass

#@receiver(pre_save, sender = MetricValue)
#def prevent_not_scheduled(sender, instance, **kwargs):

@receiver(post_save, sender = MetricValue)
def register_measurement(sender, instance, **kwargs):
    '''After new MetricValue instance is saved metricValue field of corresponding MetricValueRegistration is assigned'''
    if instance.metric.service.status=="Operational":
        mtr_val_reg = MetricValueRegistration.objects.get(metric=instance.metric, date_begin=instance.date_begin, date_end=instance.date_end)
        mtr_val_reg.metricValue = instance
        mtr_val_reg.save()

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    '''After user is logged in function looks for corresponding Staff.
     In case he is owner of some Services he remains in group ServiceMetricOwner, else he is removed.'''

    try:
        staff_id = Staff.objects.get(name = user.first_name+" "+user.last_name)
        if Service.objects.filter(owner=staff_id).count() > 0:
            user.groups.add(Group.objects.get(name='ServiceMetricOwner'))
        else:
            user.groups.remove(Group.objects.get(name='ServiceMetricOwner'))
    except Staff.DoesNotExist:

        try:
            staff = Staff.objects.get(name=user.last_name + " " + user.first_name)
            if Service.objects.filter(owner=staff).count() > 0:
                user.groups.add(Group.objects.get(name='ServiceMetricOwner'))
            else:
                user.groups.remove(Group.objects.get(name='ServiceMetricOwner'))
        except Staff.DoesNotExist:
            if Group.objects.get(name='ServiceMetricOwner') in user.groups.all():
                user.groups.remove(Group.objects.get(name='ServiceMetricOwner'))

class RemoveButtons:
    '''This is one of base classes for all model admin classes - it removes save_and_add_another and save_and_continue buttons'''
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

class SubportfolioInLine(admin.options.InlineModelAdmin):
    template = "admin/edit_inline/portfolios.html"
    model = SubPortfolio
    extra = 0
    fields = ["name"]
    readonly_fields = ["name"]
    ordering = ('order',)
    max_num = 0

class ServiceInLine(admin.options.InlineModelAdmin):
    template = "admin/edit_inline/subportfolios.html"
    model = Service
    extra = 0
    fields = ["service_name"]
    readonly_fields = ["service_name"]
    ordering = ('totalorder',)
    max_num = 0

class MetricInline(admin.options.InlineModelAdmin):
    template = "admin/edit_inline/services.html"
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

    def has_add_permission(self, request, obj):

        flag = self.cant_change_auth(request, obj)
        if flag:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):

        if self.cant_change_auth(request, obj):
            return False
        else:
            return True

    '''
    def get_readonly_fields(self, request, obj=None):


        if self.cant_change_auth(request, obj):
            return self.readonly_fields + ('value', 'date_begin', 'date_end', 'metric')

        return self.readonly_fields
    '''

    def cant_change_auth(self, request, obj):
        '''This codes determines whether User can change metricValue or not - he can if he is owner of corresponding Service and Metric or if he is superuser.'''
        if obj:

            service = Service.objects.get(id=obj.service_id)
            try:
                username = Staff.objects.get(id=service.owner_id).name
            except Staff.DoesNotExist:
                username = ""
            current_user1 = request.user.first_name + " " + request.user.last_name
            current_user2 = request.user.last_name + " " + request.user.first_name
            if not (current_user1 == username or current_user2 == username) and not request.user.is_superuser:
                return True
            else:
                return False
        else:
            return False

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(MetricValueInline, self).get_formset(
            request, obj, **kwargs)

        class PaginationFormSet(formset_class):
            '''Pagination for MetricValues as inline of metric'''
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
class PortfolioAdmin(SimpleHistoryAdmin, admin.ModelAdmin, RemoveButtons):

    inlines = [SubportfolioInLine]

    search_fields = ('name', 'design_id', 'status' )
    ordering = ('order',)

    list_display = ('design_id','name','status')
    def response_change(self, request, obj):
        return redirect(request.path)

    def __unicode__(self):
        return self.name


class SubPortfolioAdmin(SimpleHistoryAdmin, admin.ModelAdmin, RemoveButtons):

    template = "admin/edit_inline/change_form.html"
    search_fields = ( 'design_id', 'name', 'status','portfolio__name')
    ordering = ('portfolio__order','order')

    list_display = ( 'design_id', 'name', 'status',)

    inlines = [ServiceInLine,]

    def response_change(self, request, obj):
        return redirect(request.path)

    def __unicode__(self):
        return self.name

class ServiceAdmin(SimpleHistoryAdmin, admin.ModelAdmin, RemoveButtons):
    change_form_template = "admin/edit_inline/change_form.html/"
    inlines = [
        MetricInline,
    ]
    search_fields = ('service_name', 'design_id', 'owner__name', 'portfolio', 'sub_portfolio','status' )
    ordering = ('totalorder',)
    exclude = ['totalorder',]
    list_display = ('design_id','service_name','portfolio','sub_portfolio','status')

    def response_change(self, request, obj):
        return redirect(request.path)

    def __unicode__(self):
        return self.totalorder


class StaffAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
    list_display=('name','phone_number','email')
    actions=('update_staff_data',)


    def update_staff_data(self, request, queryset):
       short_description = "Update persobal data from Active Directory"
       for employee in queryset:
           employee.check_email()

    def __unicode__(self):
        return self.name

class MetricAdmin(SimpleHistoryAdmin, admin.ModelAdmin, RemoveButtons):

    change_form_template = "admin/edit_inline/change_form.html/"
    ordering = ('service__totalorder', 'metric_order', )
    search_fields = ('metric_name', 'design_id','service__design_id','service__service_name')
    inlines = [
        MetricValueInline
    ]

    list_display = ('design_id','metric_name','status','date_begin','date_end','service')
    def change_view(self, request, object_id, extra_context=None):
        '''If user is not owner of corresponding Service and Metric save and delete buttons are hidden'''
        service = Service.objects.get(id=Metric.objects.get(id=object_id).service_id)
        try:
            username = Staff.objects.get(id=service.owner_id).name
        except Staff.DoesNotExist:
            username = ""
        current_user1 = request.user.first_name + " " + request.user.last_name
        current_user2 = request.user.last_name + " " + request.user.first_name

        if Metric.objects.get(id= object_id) and not (current_user1 == username or current_user2 == username) and not request.user.is_superuser:

            extra_context = extra_context or {}
            extra_context['show_save'] = False
            extra_context['show_delete'] = False

        return super(MetricAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        '''Makes possible to edit Metric only for superusers'''
        if not request.user.is_superuser:  # editing an existing object
            return self.readonly_fields + ('service', 'design_id', 'metric_name', 'description', 'status', 'metric_order', 'publ_regularity', 'publ_deadline', 'measr_regularity', 'nature')
        return self.readonly_fields

    #readonly_fields = ['service', 'design_id', 'metric_name', 'description', 'status', 'metric_order', 'publ_regularity', 'publ_deadline', 'measr_regularity', 'nature']

    def response_change(self, request, obj):
        return redirect(request.path)

    def get_inline_formsets(self, request, formsets, inline_instances, obj=None):
        '''Makes possible to edit MetricValue inlines of Metric only for owner of corresponing Service and for superusers.'''
        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            prepopulated = dict(inline.get_prepopulated_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(
                inline, formset, fieldsets, prepopulated, readonly,
                model_admin=self,
            )

            if isinstance(inline, MetricValueInline):

                if obj:
                    service = Service.objects.get(id=obj.service_id)
                    try:
                        username = Staff.objects.get(id=service.owner_id).name
                    except Staff.DoesNotExist:
                        username = ""
                    current_user1 = request.user.first_name + " " + request.user.last_name
                    current_user2 = request.user.last_name + " " + request.user.first_name
                    if not (current_user1 == username or current_user2 == username) and not request.user.is_superuser:

                        for form in inline_admin_formset.forms:
                    # Here we change the fields read only.
                            form.fields['value'].widget.attrs['readonly'] = True
                            form.fields['metric'].widget.attrs['readonly'] = True
                            form.fields['date_begin'].widget.attrs['readonly'] = True
                            form.fields['date_end'].widget.attrs['readonly'] = True

            inline_admin_formsets.append(inline_admin_formset)
        return inline_admin_formsets
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
    search_fields=('metric__design_id','metric__service__design_id')
    list_display = ('get_metric_design_id','date_begin','date_end','value')
    ordering = ('-date_end','metric__design_id' )

    def get_metric_design_id(self, obj):
        return obj.metric.design_id

    get_metric_design_id.short_description = 'Metric Design ID'

    def get_form(self, request, obj=None, **kwargs):
        '''Restricts possible choices of Metrics when adding new MetricValue'''
        try:
            form = super(MetricValueAdmin, self).get_form(request, obj, **kwargs)
            metrics = None

            owner = Staff.objects.get(name=request.user.first_name + " " + request.user.last_name)
            for serv in Service.objects.filter(owner=owner):

                if metrics is None:
                    metrics = (Metric.objects.filter(service=serv))
                else:
                    metrics = (metrics | Metric.objects.filter(service=serv))

            form.base_fields['metric'].queryset = metrics

            return form
        except:
            return super(MetricValueAdmin, self).get_form(request, obj, **kwargs)

    def response_change(self, request, obj):
        return redirect(request.path)

    def change_view(self, request, object_id, extra_context=None):
        'Makes possible to delete and save changes to MetricValue only for corresponding ServiceMetricOwner and for supersusers'
        metric = MetricValue.objects.get(id=object_id).metric
        service = Service.objects.get(id=metric.service_id)
        username = Staff.objects.get(id=service.owner_id).name
        current_user = request.user.first_name + " " + request.user.last_name
        if MetricValue.objects.get(id=object_id) and not (current_user == username) and not request.user.is_superuser:

            extra_context = extra_context or {}
            extra_context['show_save'] = False
            extra_context['show_delete'] = False

        return super(MetricValueAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        return redirect(request.path)

    def get_readonly_fields(self, request, obj=None):
        'Makes fields of metricValue readonly for everyone except ServiceMetricOwner and superusers'
        if obj:
            metric = Metric.objects.get(id = obj.metric_id)
            service = Service.objects.get(id = metric.service_id)
            username = Staff.objects.get(id = service.owner_id).name
            if obj and not (request.user.first_name + " " + request.user.last_name == username) and not request.user.is_superuser:  # editing an existing object
                return self.readonly_fields + ('value', 'date_begin', 'date_end', 'metric')

        return self.readonly_fields

class MetricValueRegistrationAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    ordering = ('date_end',)
    search_fields = ('metric__metric_name','metric__design_id','date_begin','date_end')
    list_display = ('get_metric_design_id', 'date_begin','date_end', 'created_at', 'updated_at')
    readonly_fields = ['date_end']
    exclude= []

    def get_metric_design_id(self, obj):
        return obj.metric.design_id
    get_metric_design_id.short_description = 'Metric Design ID'

    def get_form(self, request, obj=None, **kwargs):
        try:
            form = super(MetricValueRegistrationAdmin, self).get_form(request, obj, **kwargs)

            metric_values = MetricValue.objects.filter(metric=obj.metric)
            form.base_fields['metricValue'].queryset = metric_values

            return form

        except:
            return super(MetricValueRegistrationAdmin, self).get_form(request, obj, **kwargs)

    def __unicode__(self):
        return self.name

class UserNotificationAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    ordering = ('created_at',)
    search_fields = ('subject','text','type','recipientList')
    list_display = ('type', 'subject', 'recipientList','created_at','status','attempt')
    exclude= []
    actions = ['send_notification', ]
    readonly_fields = ["status"]

    def __unicode__(self):
        return self.name



    def send_notification(self, request, queryset):
       short_description = "Send selected User notifications"
       for user_notification in queryset:
           from datetime import datetime
           now = datetime.now()

           current_time = now.strftime("%H:%M:%S")
           print(current_time, 'sending',str(user_notification))
           user_notification.delivery()

class ExternalDataSourceAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name','rdbms', 'host', 'schema', )
    list_display = ('name','rdbms', 'host', 'schema', )


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(SubPortfolio, SubPortfolioAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Metric, MetricAdmin)
admin.site.register(MetricMeasurement, SimpleHistoryAdmin)
admin.site.register(MetricValue, MetricValueAdmin)
admin.site.register(MetricValueRegistration, MetricValueRegistrationAdmin)
admin.site.register(UserNotification, UserNotificationAdmin)
admin.site.register(ExternalDataSource, ExternalDataSourceAdmin)

# Register your models here.
