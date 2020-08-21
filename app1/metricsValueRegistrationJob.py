import pytz

from django.core.mail import send_mail

from app1.models import MetricValueRegistration, Metric, ExternalDataSource
from django.db import IntegrityError
import logging

from service_catalog.settings import TIME_ZONE
from .dates_processing import *


logger = logging.getLogger(__name__)


def make_registrations(pub_regularity,date_b, date_e):


    date_begin=str(date_b)
    date_end=str(date_e)

    status = 'Operational'

    command = ''
    command += 'select * from   app1_metric'
    command += ' left join   app1_service'
    command += ' on app1_metric.service_id= app1_service.id'
    command += ' left join   app1_metricvalueregistration'
    command += ' on   app1_metric.id=  app1_metricvalueregistration.metric_id '
    command += ' and   app1_metricvalueregistration.date_begin= %s'
    command += ' and   app1_metricvalueregistration.date_end= %s'
    command += ' where   app1_service.status=%s'
    command += ' and   app1_metric.status=%s'
    command += ' and   app1_metricvalueregistration.id is Null'
    command += '  and   app1_metric.date_begin<=%s'
    command += '  and   app1_metric.date_end>=%s'
    command += '  and   app1_metric.publ_regularity=%s'
    metrics = Metric.objects.raw(command, [date_begin, date_end, status, status, date_end, date_begin,pub_regularity])

    for metric in metrics:
        try:
            MetricValueRegistration.objects.create(metric=metric, date_begin=date_begin, date_end=date_end)
            print(MetricValueRegistration.objects.count())
        except IntegrityError:
            message = 'Attempt to add registration with identical dates and metric to already existing. Metric: " ' + str(metric) + ", measurement dates: " +\
            str(date_begin) + ' - ' + str(date_end)
            logger.error(message)

def checkMetrixValueRegistration():

    now = datetime.now()

    yesterday = get_yesterday(now)
    make_registrations('daily',yesterday.replace(hour=0, minute=0, second=0, microsecond=0), yesterday )


    yesterday = now - timedelta(days=7)
    if True or yesterday == first_last_day_of_week(yesterday)['last']:
        make_registrations('weekly',first_last_day_of_week(yesterday)['first'], first_last_day_of_week(yesterday)['last'])

    yesterday = first_last_day_of_month(now)['first'] - timedelta(days=1)
    if True or yesterday == first_last_day_of_month(yesterday)['last'] :
        make_registrations('monthly',first_last_day_of_month(yesterday)['first'], first_last_day_of_month(yesterday)['last'])

    yesterday = first_last_day_of_quartal(now)['first'] - timedelta(days=1)


    if True or yesterday == first_last_day_of_quartal(yesterday)['last']:
        make_registrations('quaterly',first_last_day_of_quartal(yesterday)['first'], first_last_day_of_quartal(yesterday)['last'])

    yesterday = first_last_day_of_half_year(now)['first'] - timedelta(days=1)
    if True or yesterday == first_last_day_of_half_year(yesterday)['last']:
        make_registrations('half-year',first_last_day_of_half_year(yesterday)['first'], first_last_day_of_half_year(yesterday)['last'])

    yesterday = first_last_day_of_year(now)['first'] - timedelta(days=1)
    if True or yesterday == first_last_day_of_year(yesterday)['last']:
        make_registrations('yearly',first_last_day_of_year(yesterday)['first'], first_last_day_of_year(yesterday)['last'])



def checkMetrixValueDeadLines():
    MetricValueRegistration.checkDeadLines()


def importMetricMeasurement():
    for source in ExternalDataSource.objects.filter(table__iexact=''):
        source.importMetricMeasurement
