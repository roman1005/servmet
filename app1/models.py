from email.headerregistry import Group

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User, _user_has_module_perms, _user_has_perm, _user_get_permissions, Permission, \
    UserManager
import uuid

from django.db.models.manager import EmptyManager
from phone_field import PhoneField
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


STATUS_CHOICES = (
    ('DEF', 'Defined'),
    ('SUB', 'Submited'),
    ('DEP', 'Deployed'),
    ('OP', 'Operational'),
    ('RETU', 'Retired(Upgrade)'),
    ('RETR', 'Retired(Replacemenet)'),
    ('RETO', 'Retired(Obsolete)'),
    ('CANU', 'Cancelled(Upgrade)'),
    ('CANR', 'Cancelled(Replacemenet)'),
    ('EXT', 'External premises'),
    ('UNCO', 'Under consideration'),
    ('UNK', 'Unknown'),
    ('DIS', 'Displaced'),
    ('NA', 'Not agreed'),
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
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='DEF')
    totalorder = models.CharField( max_length=100, blank=True, null=True, verbose_name="Total order")
    history = HistoricalRecords()

    def __str__(self):
        return str(self.design_id) + "--" + self.service_name + " { " + self.portfolio + " -> " + self.sub_portfolio + " }"

class Metric(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    design_id = models.IntegerField(default=0)
    metric_name = models.CharField(max_length=100)
    description = models.TextField()
    date_begin = models.DateTimeField(auto_now=True, null=True)
    date_end = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='DEF')
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
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT,  blank=-False)
    value = models.FloatField(verbose_name="Metric value")
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    history = HistoricalRecords()
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




