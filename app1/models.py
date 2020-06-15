from django.db import models
from django.contrib.auth.models import User
import uuid
from phone_field import PhoneField
from simple_history.models import HistoricalRecords

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

class Owner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone_number = PhoneField()
    email = models.EmailField(max_length=100)

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone_number = PhoneField()
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name + "" + self.lastname

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
    design_id = models.IntegerField( unique=True)
    service_name = models.CharField(unique=True, max_length=100)
    portfolio = models.CharField(max_length=250)
    sub_portfolio = models.CharField(max_length=250)
    customer = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='customerID',blank=True, null=True)
    owner = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='ownerID', blank=True, null=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='DEF')
    totalorder = models.CharField( max_length=100, blank=True, null=True, verbose_name="Total order")
    history = HistoricalRecords()

    def __str__(self):
        return self.service_name + " { " + self.portfolio + " -> " + self.sub_portfolio + " }"

class Metric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    metric_name = models.CharField(max_length=100)
    description = models.TextField()
    date_begin = models.DateTimeField(auto_now=True, null=True)
    date_end = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='DEF')
    metric_order = models.IntegerField()
    nature = models.CharField(max_length=300)
    publ_regularity = models.CharField(max_length=100, default="", verbose_name='Publication Regularity')
    publ_deadline = models.CharField(max_length=100, default="", verbose_name='Publication Deadline')
    measr_regularity = models.CharField(max_length=100, default="", verbose_name='Measure Regularity')

    history = HistoricalRecords()

    def __str__(self):
        return self.metric_name

class MetricMeasurement(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    history = HistoricalRecords()

class MetricValue(models.Model):

    class Meta:
        verbose_name = "Metric value"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric= models.ForeignKey(Metric, on_delete=models.PROTECT,  blank=-False)
    value = models.IntegerField(verbose_name="Metric value", default=-1)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # get number of items that have an overlapping start date
        metric_value_overlapping_start = MetricValue.objects.filter(date_begin__gte=self.date_begin,
                                                                          date_begin__lte=self.date_end).count()

        # get number of items that have an overlapping end date
        metric_value_overlapping_end = MetricValue.objects.filter(date_end__gte=self.date_begin,
                                                                        date_end__lte=self.date_end).count()

        overlapping_metric_value_present = metric_value_overlapping_start > 0 or metric_value_overlapping_end > 0

        if overlapping_metric_value_present:
            print("Trying to overlap metric value")
            #metric = Metric.objects.get(metric_name = self.metric)
            #return redirect('http://127.0.0.1:8000/admin/app1/metric/6b6ad711-f536-42dd-b4d2-000c98dda3e6/change/')
        else:
            super(MetricValue, self).save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return "--" + str(self.date_begin) + " - " + str(self.date_end) + " {" + str(self.value) + "}"


