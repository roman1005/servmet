from app1.models import MetricValueRegistration, Metric
from django.db import IntegrityError
import logging

from .dates_processing import *

logger = logging.getLogger(__name__)


def make_registrations(date_begin, date_end):

    status = 'Under consideration'

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

    metrics = Metric.objects.raw(command, [date_begin, date_end, status, status, date_end, date_begin])

    for metric in metrics:
        try:
            MetricValueRegistration.objects.create(metric=metric, date_begin=date_begin, date_end=date_end)
            print(MetricValueRegistration.objects.all().count())
        except IntegrityError:
            message = 'Attempt to add registration with identical dates and metric to already existing. Metric: " ' + str(metric) + ", measurement dates: " +\
            str(date_begin) + ' - ' + str(date_end)
            logger.error(message)

def checkMetrixValueRegistration():

    now = datetime.now()

    yesterday = get_yesterday(now)

    periods = ['week', 'month', 'quartal', 'half_year', 'year']

    if yesterday == first_last_day_of_week(yesterday)['last']:
        make_registrations(first_last_day_of_week(yesterday)['first'], first_last_day_of_week(yesterday)['last'])

    elif yesterday == first_last_day_of_month(yesterday)['last']:
        make_registrations(first_last_day_of_month(yesterday)['first'], first_last_day_of_month(yesterday)['last'])

    elif yesterday == first_last_day_of_quartal(yesterday)['last']:
        make_registrations(first_last_day_of_quartal(yesterday)['first'], first_last_day_of_quartal(yesterday)['last'])

    elif yesterday == first_last_day_of_half_year(yesterday)['last']:
        make_registrations(first_last_day_of_half_year(yesterday)['first'], first_last_day_of_half_year(yesterday)['last'])

    elif yesterday == first_last_day_of_year(yesterday)['last']:
        make_registrations(first_last_day_of_year(yesterday)['first'], first_last_day_of_year(yesterday)['last'])



    current_time = now.strftime("%H:%M:%S")
    print("Metrix check", current_time)