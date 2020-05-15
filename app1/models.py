from django.db import models
from django.contrib.auth.models import User
import uuid
from phone_field import PhoneField
from simple_history.models import HistoricalRecords

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
        return self.name + "" + self.surname

class Staff(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone_number = PhoneField()
    email = models.EmailField(max_length=100)
    table_number = models.IntegerField(unique=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name + " " + self.surname

class Service_CI(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    design_id = models.IntegerField(default=0, unique=True)
    service_name = models.CharField(unique=True, max_length=100)
    portfolio = models.CharField(max_length=250)
    sub_portfolio = models.CharField(max_length=250)
    customer = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='customer')
    owner = models.ForeignKey(Staff,  on_delete=models.CASCADE, related_name='owner')

    history = HistoricalRecords()

    def __str__(self):
        return self.service_name

# Create your models here.
