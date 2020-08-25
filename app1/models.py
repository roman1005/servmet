


from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User, Permission
import uuid



from phone_field import PhoneField
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from app1.dates_processing import *
#from app1.ldapSearch import get_ldap_mail
from app1.validators import *

STATUS_CHOICES = (
    ('Defined', 'Defined'),
    ('Submited', 'Submited'),
    ('Deployed', 'Deployed'),
    ('Operational', 'Operational'),
    ('Retired(Upgrade)', 'Retired(Upgrade)'),
    ('Retired(Replacemenet)', 'Retired(Replacemenet)'),
    ('Retired(Obsolete)', 'Retired(Obsolete)'),
    ('Cancelled(Upgrade)', 'Cancelled(Upgrade)'),
    ('Cancelled(Replacemenet)', 'Cancelled(Replacemenet)'),
    ('External premises', 'External premises'),
    ('Under consideration', 'Under consideration'),
    ('Unknown', 'Unknown'),
    ('Displaced', 'Displaced'),
    ('Not agreed', 'Not agreed'),
)


REGULARITY_CHOICES = (
    ('',''),
    ('daily','daily'),
    ('weekly','weekly'),
    ('monthly','monthly'),
    ('quaterly','quaterly'),
    ('half-year','half-year'),
    ('yearly', 'yearly'),
)


MEASUREMENT_CHOICES = (

    ('sec','sec'),
    ('min','min'),
    ('hour','hour'),
    ('day','day'),
    ('week','week'),
    ('month','month'),
    ('quarter','quarter'),
    ('half-year','half-year'),
    ('year', 'year'),
)
SYSTEM_NOTIFICATION_CHOICES = (
    ('INFO','INFO'),
    ('WARNING','WARNING'),
    ('ALERT','ALERT'),

)
RDBMS_TYPES_CHOICES = (
    ('MySQL','MySQL'),
    ('Oracle','Oracle'),
    ('MS SQL','MS SQL Server'),

)
class Staff(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    phone_number = PhoneField(blank=True, null=True)
    email = models.EmailField(max_length=100,blank=True, null=True)

    history = HistoricalRecords()
    '''
    def check_email(self):
        if self.email is None or self.email=='':
            name = self.name.split()
            mail = get_ldap_mail(name[0], name[1])
            if mail is None:
                mail = get_ldap_mail(name[1], name[0])

            if mail is not None:
                self.email = mail
                self.save()
    '''
    def __str__(self):
        return self.name


class ExternalDataSource(models.Model):
    class Meta:
        verbose_name = "External Data Source"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    rdbms = models.CharField(max_length=30, choices=RDBMS_TYPES_CHOICES)
    schema = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    history = HistoricalRecords()
    datasource_admin_mails=models.EmailField(blank=False, null=True)
    table= models.CharField(max_length=100,default='')

    time_slot_begin = models.TimeField(blank=True, null=True, default='00:00:00',
                                       verbose_name='Start of allowed timeslot')
    time_slot_end = models.TimeField(blank=True, null=True, default='23:59:59',
                                     verbose_name='Start of allowed timeslot')
    lastExtraction=models.DateTimeField(default=datetime.now()-timedelta(days=1),verbose_name='last daily extraction')

    def __str__(self):
        return str(self.name) + "  -  " + str(self.host) + " - " + str(self.schema)
    def toEmail(self):
        text = '\nhost--' + self.host + ':' + str(self.port)
        text += '\nschema--' + self.schema
        return text

    'import metricMeasuwment from the datasource'
    def importMetricMeasurement(self):
        if self.lastExtraction+timedelta(days=1)<datetime.now() and self.table!='':
            self.lastExtraction=datetime.now()
            self.save()


class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    design_id = models.IntegerField(unique=True)
    name=models.CharField(unique=True, max_length=200)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='Under consideration')
    description = models.TextField(null=True, blank=True)
    order=models.IntegerField(default=999)
    portfolioRed=models.IntegerField(default=0,validators=[validateRGB],verbose_name='Portfolio RED(RGB)')
    portfolioGreen = models.IntegerField(default=0, validators=[validateRGB], verbose_name='Portfolio GREEN(RGB)')
    portfolioBlue = models.IntegerField(default=0, validators=[validateRGB], verbose_name='Portfolio BLUE(RGB)')
    sub_portfolioRed = models.IntegerField(default=0, validators=[validateRGB], verbose_name='SubPortfolio RED(RGB)')
    sub_portfolioGreen = models.IntegerField(default=0, validators=[validateRGB], verbose_name='SubPortfolio GREEN(RGB)')
    sub_portfolioBlue = models.IntegerField(default=0, validators=[validateRGB], verbose_name='SubPortfolio BLUE(RGB)')
    refCard = models.URLField(null=True, blank=True, verbose_name='Link to RefCard')
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class SubPortfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    design_id = models.IntegerField(unique=True)
    name=models.CharField(unique=True, max_length=200)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='Under consideration')
    description = models.TextField(null=True, blank=True)
    order=models.IntegerField(default=999)
    portfolio=models.ForeignKey(Portfolio,on_delete=models.PROTECT)
    refCard = models.URLField(null=True, blank=True, verbose_name='Link to RefCard')

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Service(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    design_id = models.IntegerField(unique=True)
    service_name = models.CharField(unique=True, max_length=200)
    portfolio = models.CharField(max_length=250)
    sub_portfolio = models.CharField(max_length=250)
    subportfolio = models.ForeignKey(SubPortfolio, on_delete=models.PROTECT, related_name='subPortfolio', blank=True,
                                     null=True)
    customer = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='customerID',blank=True, null=True)
    owner = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='ownerID', blank=True, null=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='Under consideration')
    description=models.TextField(null=True,blank=True)
    totalorder = models.CharField( max_length=100, blank=True, null=True, verbose_name="Total order")
    history = HistoricalRecords()
    notification_on = models.BooleanField(default=True, blank=True, null=True, verbose_name='Notification on')
    alerts_on = models.BooleanField(default=True, blank=True, null=True, verbose_name='Alerts on')
    refCard = models.URLField(null=True, blank=True, verbose_name='Link to RefCard')
    architecture = models.URLField(null=True, blank=True, verbose_name='Architecture')
    _isNew = True
    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could
        # be replaced with super()).
        instance=super().from_db(db,field_names,values)
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        instance._isNew=False
        return instance

    def save(self,*args, **kwargs):
        #below we check if service is changing its status  into Operational
        changeStatus=''
        metricCheckNotification=''
        if (self._isNew or self.status != self._loaded_values['status']) and self.status=='Operational':
            changeStatus = 'InProd'
        elif self._isNew==False and self.status != self._loaded_values['status'] and self._loaded_values['status']=='Operational':
            changeStatus = 'OutProd'
        super(Service, self).save(*args, **kwargs)

        if changeStatus!='':
            self.issueServiceOwnerNotification(changeStatus)


            for metric in Metric.objects.filter(service__id=self.id, status='Operational'):
                metric.issueMetricStateNotification(changeStatus)
                if metric.extract_from_sql_datasource:
                    metric.issueMetricCheckNotification(changeStatus)


        #checkProdMetrix
    def __str__(self):
        return self.service_name +'[' +str(self.design_id)+"] { " + self.portfolio + " -> " + self.sub_portfolio + " }"

    def issueServiceOwnerNotification(self, template: str):

        serviceOwner = Staff.objects.get(pk=self.owner_id)
        serviceOwner.check_email()
        subject = 'Service [' + str(self.design_id) + ']'
        if template == 'InProd':
            subject += ' in operational status'
            text = 'Dear Service Owner! \n\n Please be informed that service ' + self.__str__() + '\n changed its status to operational.\n\n'
            text = text + 'Please visit https://metrix.com/admin/app1/service/' + str(self.id)
        if template == 'OutProd':
            subject += ' in non-operational status'
            text = 'Dear Service Owner! \n\n Please be informed that service' + self.__str__() + ' changed its status from operational.\n\n'
            text = text + 'Please visit https://metrix.com/admin/app1/service/' + str(self.id)

        notification = UserNotification.objects.create(subject=subject, recipientList=serviceOwner.email, text=text)
        notification.save()

class Metric(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    design_id = models.IntegerField(default=0)
    metric_name = models.CharField(max_length=100)
    description = models.TextField( blank=True,null=True)
    date_begin = models.DateTimeField( null=True)
    date_end = models.DateTimeField(null=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='Under consideration')
    metric_order = models.IntegerField(default=9999)
    nature = models.CharField(max_length=300)
    publ_regularity = models.CharField(max_length=100, choices=REGULARITY_CHOICES, default="", verbose_name='Publication Regularity', blank=True)
    publ_deadline = models.IntegerField(default="0", verbose_name='Publication Deadline,days', blank=True)
    measr_period = models.IntegerField(default=0, verbose_name='Measurement Regularity period', blank=True)
    measr_regularity = models.CharField(max_length=100, choices=MEASUREMENT_CHOICES, default="", verbose_name='Measurement Regularity unit', blank=True,null=True)
    extract_from_sql_datasource=models.BooleanField(blank=True, null=True, default=False, verbose_name='Extract Values from SQL-datascource')
    data_source=models.ForeignKey(ExternalDataSource, on_delete=models.PROTECT,blank=True,null=True)
    sql_command=models.TextField(default='', blank=True,null=True)
    sql_extraction_delay= models.IntegerField(blank=True, null=True,default=-1, verbose_name='Delay from the the end of period, hours')
    time_slot_begin= models.TimeField (blank=True, null=True,default='00:00:00',verbose_name='Start of allowed timeslot')
    time_slot_end=models.TimeField (blank=True, null=True,default='23:59:59',verbose_name='Start of allowed timeslot')

    history = HistoricalRecords()
    _isNew=True

    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could
        # be replaced with super()).
        instance = super().from_db(db, field_names, values)
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        instance._isNew=False
        return instance

    def clean(self):
        error_txt=''
        if self.extract_from_sql_datasource and self.status=='Operational':
            if self.data_source is None or self.sql_command is None or self.sql_command==''\
                or self.sql_extraction_delay is None or self.sql_extraction_delay<0 \
                or self.time_slot_begin is None or self.time_slot_end is None \
                or self.time_slot_begin>=self.time_slot_end:
                    error_txt='Please specify all and correct parameters for metric value extraction or cancel it.'

        if error_txt!='':
            raise ValidationError('Please specify all and correct parameters for metric value extraction or cancel it.')

    def save(self, *args, **kwargs):
        # below we check if service is changing its status  into Operational
        super(Metric, self).save(*args, **kwargs)
        if self.service.status=='Operational':
            changeStatusInOperational = False
            changeStatusOutOperational = False
            if (self._isNew or self.status != self._loaded_values['status']) and self.status == 'Operational':
                changeStatusInOperational = True
            elif self._isNew==False and self.status != self._loaded_values['status'] and self._loaded_values['status'] == 'Operational':
                changeStatusOutOperational = True
            super(Metric, self).save(*args, **kwargs)

            if changeStatusInOperational:
                self.issueMetricStateNotification('InProd')
                if self.extract_from_sql_datasource:
                    self.issueMetricCheckNotification('InPord')

            if changeStatusOutOperational:
                self.issueMetricStateNotification('OutProd')
                if self._loaded_values['extract_from_sql_datasource']:
                    self.issueMetricCheckNotification('OutProd')

            if self._isNew==False and self.status == 'Operational' and self.status == self._loaded_values['status']: #check if  extraction changed
                if str(self.data_source_id)!=str(self._loaded_values['data_source_id']) or self.sql_extraction_delay!= self._loaded_values['sql_extraction_delay']\
                    or self.sql_command!= self._loaded_values['sql_command'] or self.extract_from_sql_datasource!=self._loaded_values['extract_from_sql_datasource'] \
                    or self.time_slot_begin!= self._loaded_values['time_slot_begin'] or self.time_slot_end!=self._loaded_values['time_slot_end'] \
                    or self.data_source_id!=self._loaded_values['data_source_id']  \
                    or self.sql_extraction_delay!=self._loaded_values['sql_extraction_delay']:
                        if self.extract_from_sql_datasource :
                            self.issueMetricCheckNotification('InProd')
                            if self.data_source_id!=self._loaded_values['data_source_id']:
                                self.issueMetricCheckNotification('OutProd')# old DataSourceOwner Should be notified
                        else:
                            self.issueMetricCheckNotification('OutProd')
    def __str__(self):
        return  str(self.metric_name)+'['+str(self.design_id)+']'

    def issueMetricCheckNotification(self, template: str):
        serviceOwner = Staff.objects.get(pk=self.service.owner.id)
        serviceOwner.check_email()
        sourceOwner_mail = self.data_source.datasource_admin_mails
        subject = subject = 'Metric [' + str(self.design_id) + '] values extraction'
        text = 'Dear Data Source and Service owners! \n\n Please be informed that values of a metric\n' + self.__str__()
        text += '\nService --' + self.service.__str__()
        if template == 'InProd':
            subject += ' is operational'
            ds = ExternalDataSource.objects.get(pk=self.data_source_id)
            text += '\n will be extracted from data source ' + ds.toEmail()+':'


            text += '\n\n\nSQL-command-- ' + self.sql_command

            text += '\n\nperiod--' + self.measr_regularity
            text += '\ndelay from the end of a period,hours--' + str(self.sql_extraction_delay)
            text += '\nextraction time slot--from ' + self.time_slot_begin.strftime(
                "%H:%M:%S.%f") + ' till ' + self.time_slot_end.strftime("%H:%M:%S.%f")

        elif template == 'OutProd':
            subject += ' is non-operational'
            ds = ExternalDataSource.objects.get(pk=self._loaded_values['data_source_id'])

            text += '\n will not be extracted from data source ' + ds.toEmail() + ':'
            text += '\n\n\nSQL-command--' + self._loaded_values['sql_command']
            text += '\n\nperiod--' + self._loaded_values['measr_regularity']
            text += '\ndelay from the end of a period,hours--' + str(self._loaded_values['sql_extraction_delay'])
            text += '\nextraction time slot--from ' + self._loaded_values['time_slot_begin'].strftime(
                "%H:%M:%S.%f") + ' till ' + self._loaded_values['time_slot_end'].strftime("%H:%M:%S.%f")
        text = text + '\nPlease visit https://metrix.com/admin/app1/metric/' + str(self.id)
        notification = UserNotification.objects.create(subject=subject,
                                                       recipientList=sourceOwner_mail + ',' + serviceOwner.email,
                                                       text=text)
        notification.save()

    def issueMetricStateNotification(self, template: str):
        if self.service.alerts_on:
            serviceOwner = Staff.objects.get(pk=self.service.owner.id)
            serviceOwner.check_email()
            subject = 'Metric [' + str(self.design_id) + ']'
            text = 'Dear Service Owner! \n\n Please be informed that metric\n' + self.metric_name
            if template == 'InProd':
                subject += ' is operational'
                text += '\n changed its status to operational.\n\n'

            if template == 'OutProd':
                subject += ' is non-operational'
                text += '\n changed its status from operational.\n'

            text = text + 'Please visit https://metrix.com/admin/app1/metric/' + str(self.id)
            notification = UserNotification.objects.create(subject=subject, recipientList=serviceOwner.email, text=text)
            notification.save()

class MetricMeasurement(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT, null=False)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    timestamp = models.DateTimeField()
    measurement = models.FloatField()
    dataSource = models.ForeignKey(ExternalDataSource, on_delete=models.PROTECT, null=True)
    flg_valid = models.BooleanField(default=False)
    history = HistoricalRecords()

class MetricValue(models.Model):

    class Meta:
        verbose_name = "Metric value"
        unique_together = ('metric', 'date_begin', 'date_end',)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT,  blank=False)
    value = models.FloatField(verbose_name="Metric value")
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField(blank=True)

    history = HistoricalRecords()
    
    #def save(self, *args, **kwargs):
    def clean(self):
        # below we correct period in accordance with publication regularity
        if self.metric.publ_regularity.lower() == 'weekly':
            period = first_last_day_of_week(self.date_begin)
        elif self.metric.publ_regularity.lower() == 'monthly':
            period = first_last_day_of_month(self.date_begin)
        elif self.metric.publ_regularity.lower() == 'quarterly':
            period = first_last_day_of_quartal(self.date_begin)
        elif self.metric.publ_regularity.lower() == 'half-year':
            period = first_last_day_of_half_year(self.date_begin)
        elif self.metric.publ_regularity.lower() == 'yearly':
            period = first_last_day_of_year(self.date_begin)
        else: raise ValidationError("Unsupported publication regularity:<"+self.metric.publ_regularity+'>.')
        self.date_begin=period["first"]
        self.date_end=period["last"]
        if self.metric.service.status=='Operational': #validation only for services in operational state
            numb = MetricValueRegistration.objects.filter(metric=self.metric).count()
            if numb == 0 :
                raise ValidationError("Measurement of metric value for this metric isn't scheduled")
            else:
                if MetricValueRegistration.objects.filter(metric=self.metric,
                                                                           date_begin=self.date_begin,
                                                                           date_end=self.date_end).count() == 1: #it can be either 0 or 1 because of unique_together
                   registration = MetricValueRegistration.objects.get(metric=self.metric,
                                                                           date_begin=self.date_begin,
                                                                           date_end=self.date_end)
                   if registration.metricValue is not None:
                       raise ValidationError("Measurement of metric value for this metric on these datetimes have already been done")
                else:
                    raise ValidationError("Measurement of metric value for this metric on these datetimes isn't scheduled")

        #super(MetricValue, self).save(*args, **kwargs)
    '''
    def save(self, *args, **kwargs):
        # get number of items that have an overlapping start date
        metric_value_overlapping_start = MetricValue.objects.filter(date_begin__gte=self.date_begin,
                                                                    date_begin__lte=self.date_end).count()

        # get number of items that have an overlapping end date
        metric_value_overlapping_end = MetricValue.objects.filter(date_end__gte=self.date_begin,
                                                                  date_end__lte=self.date_end).count()

        overlapping_metric_value_present = metric_value_overlapping_start > 0 or metric_value_overlapping_end > 0

        if overlapping_metric_value_present:
            # print("Trying to overlap metric value")
            raise ValidationError('Date begin or date end field overlaps with other metric values.')
        elif self.date_begin > self.date_end:
            raise ValidationError('Date begin cannot be later than date end.')
        else:
            super(MetricValue, self).save(*args, **kwargs)
    '''


    def __str__(self):
        design_id = Metric.objects.get(id=self.metric_id).design_id
        return str(design_id) + "--" + str(self.date_begin) + " - " + str(self.date_end) + " {" + str(self.value) + "}"


class MetricValueRegistration (models.Model):
    class Meta:
        verbose_name = "Metric value registration"
        unique_together = ('metric', 'date_begin', 'date_end',)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    metricValue = models.ForeignKey (MetricValue, on_delete=models.PROTECT, blank=True, null=True)
    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Updated at')

    _isNew = True

    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could
        # be replaced with super()).
        instance = super().from_db(db, field_names, values)
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        instance._isNew = False
        return instance

    def __str__(self):
        design_id = Metric.objects.get(id=self.metric_id).design_id
        return '['+str(design_id) + "]--" + str(self.date_begin) + " - " + str(self.date_end)
    def save(self,*args, **kwargs):
        super(MetricValueRegistration, self).save(*args, **kwargs)
        if self._isNew and self.metric.service.alerts_on:
            self.issueMetricSchedulingNotifications()
    def issueMetricSchedulingNotifications(self):
        subject='metric reminder '+ self.__str__()
        text='Dear Service owner!\n'
        text+='Please be informed that registration of metric value is scheduled:\n\n'

        text += self.toEmail()

        notification = UserNotification.objects.create(subject=subject,
                                                       recipientList=self.metric.service.owner.email,
                                                       text=text)
        notification.save()

    @classmethod
    def checkDeadLines(cls):
        #process only not matched registrations
        for metric in MetricValueRegistration.objects.filter(metricValue__value__isnull=True):
            metric.issueMetricDeadLineNotification()
    def issueMetricDeadLineNotification(self):
        #check that deadline is passed
        if self.date_end+timedelta(days=self.metric.publ_deadline)<datetime.now():
            #check that today notification was not send today or it's just created
            if self.updated_at.date()<datetime.today().date() or self.updated_at-timedelta(seconds=1)<self.created_at:
                subject='metric issue '+self.__str__()
                #save time notification delivery
                self.save(force_update=True)
                text = 'Dear Service owner!\n'
                text += 'Please be informed that registration of metric value in-time is failed.\n\n'

                text += self.toEmail()

                notification = UserNotification.objects.create(subject=subject,
                                                               recipientList=self.metric.service.owner.email,
                                                               text=text)
    def toEmail(self):
        text = 'Service--' + self.metric.service.service_name + '[' + str(self.metric.service.design_id) + ']\n'
        text += 'Metric--' + self.metric.metric_name + '[' + str(self.metric.design_id) + ']\n'
        text += 'Time slot--from ' + self.date_begin.__str__()+ ' till ' + self.date_end.__str__()+ '\n'
        text += 'Publication deadline, days -- ' + str(self.metric.publ_deadline)
        return text

class UserNotification(models.Model):
    class Meta:
        verbose_name = "User notification"


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=30, choices=SYSTEM_NOTIFICATION_CHOICES, default='INFO')
    text= models.TextField(verbose_name="Content")
    subject = models.CharField(max_length=100)
    recipientList=models.CharField(max_length=250,verbose_name="To")
    history = HistoricalRecords()
    status = models.IntegerField(verbose_name="Delivery status", blank=True, null=True, default=-1)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Updated at')
    attempt = models.IntegerField(default=0)

    def __str__(self):
         return str(self.recipientList) + "  -  " + str(self.subject) + " - " + str(self.created_at)

    def delivery(self):
        # chek that some time passed before next attempt progressive delay: 0,2,6,12,20...hours
        if self.created_at+timedelta(hours=self.attempt*(self.attempt+1))<datetime.now():
            self.attempt = self.attempt + 1
            self.save()
            self.status = send_mail(
                '[' + self.type + ']' + self.subject,
                self.text,
                'noreply@metrix.com',
                self.recipientList.split(','),
                fail_silently=True
            )

            self.save()
