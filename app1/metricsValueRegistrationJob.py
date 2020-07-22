from app1.models import MetricValueRegistration, Metric, Service
from datetime import datetime, timedelta
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)

def is_quartal(date):

    if date.month == 3 and date.day == 31:
        date_begin = datetime.now()
        date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=1)
        return {"res": True, "begin": date_begin}

    elif date.month == 6 and date.day == 30:
        date_begin = datetime.now()
        date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=4)
        return {"res": True, "begin": date_begin}

    elif date.month == 9 and date.day == 30:
        date_begin = datetime.now()
        date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=7)
        return {"res": True, "begin": date_begin}

    elif date.month == 12 and date.day == 31:
        date_begin = datetime.now()
        date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=10)
        return {"res": True, "begin": date_begin}

    else:
        return {"res": False}

def is_half_year(date):

    if date.month == 6 and date.day == 30:
        date_begin = datetime.now()
        date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=1)
        return {"res": True, "begin": date_begin}

    elif date.month == 12 and date.day == 31:
        date_begin = datetime.now()
        date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=7)
        return {"res": True, "begin": date_begin}

    else:
        return {"res": False}

def end_period(now, period):

    today23pm = now.replace(hour=23, minute=0, second=0, microsecond=0)

    if now.time() > today23pm.time():

        if now.date().weekday() == 6 and period == 'week':
            date_begin = now - timedelta(days=now.weekday(), weeks=0)
            date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0)
            return {"res": True, "begin": date_begin}

        elif now.date == last_day_of_month(now) and period == 'month':
            date_begin = now.replace(day=1)
            date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0)
            return {"res": True, "begin": date_begin}

        elif is_quartal(now)['res'] == True and period == 'quartal':
            return is_quartal(now)

        elif is_half_year(now)['res'] == True and period == 'half_year':
            return is_half_year(now)

        elif now.month == 12 and now.day == 31:

            date_begin = datetime.now()
            date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=1)
            return {"res": True, "begin": date_begin}

        else:
            return {"res": False}

    else:
        return {"res": False}

from app1.models import UserNotification

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
    date_end = now.replace(hour=23, minute = 0, second=0, microsecond=0)

    periods = ['week', 'month', 'quartal', 'half_year', 'year']

    '''
    for service in Service.objects.all():
        print(service.status)
    '''

    for period in periods:
        if end_period(now, period)["res"]:
            date_begin = end_period(now, period)['begin']
            make_registrations(date_begin, date_end)

    current_time = now.strftime("%H:%M:%S")
    print("Metrix check", current_time)



def notifyUsers():
   for user_notification in UserNotification.objects.get(status__isnull=True):
        print(user_notification.text)