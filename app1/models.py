from email.headerregistry import Group

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User, _user_has_module_perms, _user_has_perm, _user_get_permissions, Permission, \
    UserManager
import uuid
from django.http import HttpResponse
from django.db.models.manager import EmptyManager
from phone_field import PhoneField
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
SYSTEM_NOTIFICATION_CHOICES = (
    ('INFO','INFO'),
    ('WARNING','WARNING'),
    ('ALERT','ALERT'),

)
class Staff(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    phone_number = PhoneField(blank=True, null=True)
    email = models.EmailField(max_length=100,blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Service(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    design_id = models.IntegerField(unique=True)
    service_name = models.CharField(unique=True, max_length=100)
    portfolio = models.CharField(max_length=250)
    sub_portfolio = models.CharField(max_length=250)
    customer = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='customerID',blank=True, null=True)
    owner = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='ownerID', blank=True, null=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='Defined')
    totalorder = models.CharField( max_length=100, blank=True, null=True, verbose_name="Total order")
    history = HistoricalRecords()
    notification_on = models.BooleanField(default=True, blank=True, null=True, verbose_name='Notification on')
    alerts_on = models.BooleanField(default=True, blank=True, null=True, verbose_name='Alerts on')

    def __str__(self):
        return str(self.design_id) + "--" + self.service_name + " { " + self.portfolio + " -> " + self.sub_portfolio + " }"

class Metric(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    design_id = models.IntegerField(default=0)
    metric_name = models.CharField(max_length=100)
    description = models.TextField()
    date_begin = models.DateTimeField( null=True)
    date_end = models.DateTimeField(null=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='DEF')
    metric_order = models.IntegerField()
    nature = models.CharField(max_length=300)
    publ_regularity = models.CharField(max_length=100, choices=REGULARITY_CHOICES, default="", verbose_name='Publication Regularity', blank=True)
    publ_deadline = models.CharField(max_length=100, default="", verbose_name='Publication Deadline', blank=True)
    measr_regularity = models.CharField(max_length=100, default="", verbose_name='Measure Regularity')

    history = HistoricalRecords()

    def __str__(self):
        return str(self.design_id) + "--" + str(self.metric_name)


class MetricMeasurement(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    history = HistoricalRecords()

class MetricValue(models.Model):

    class Meta:
        verbose_name = "Metric value"
        unique_together = ('metric', 'date_begin', 'date_end',)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT,  blank=False)
    value = models.FloatField(verbose_name="Metric value")
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    history = HistoricalRecords()
    
    def save(self, *args, **kwargs):
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

        super(MetricValue, self).save(*args, **kwargs)
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

    @classmethod
    def create(cls, metric, date_begin, date_end):
        mtrc_val_reg = cls(metric=metric, date_begin=date_begin, date_end=date_end)
        # do something with the book
        return mtrc_val_reg

    def __str__(self):
        design_id = Metric.objects.get(id=self.metric_id).design_id
        return str(design_id) + "--" + str(self.date_begin) + " - " + str(self.date_end)

class UserNotification(models.Model):
    class Meta:
        verbose_name = "User notification"


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=30, choices=SYSTEM_NOTIFICATION_CHOICES, default='INFO')
    text= models.TextField(verbose_name="Content")
    subject = models.CharField(max_length=100)
    recipientList=models.TextField(verbose_name="To")
    history = HistoricalRecords()
    status = models.FloatField(verbose_name="Delivery status", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Updated at')

    def __str__(self):
         return str(self.recipientList) + "  -  " + str(self.subject) + " - " + str(self.created_at)
