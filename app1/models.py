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
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    history = HistoricalRecords()



