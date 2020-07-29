from datetime import timedelta, datetime

def first_last_day_of_month(any_day_of_month):

    '''returns first and last day of month by any day of this month as dictionary'''
    next_month = any_day_of_month.replace(day=28) + timedelta(days=4)
    last_day = next_month - timedelta(days=next_month.day)
    last_day = last_day.replace(hour = 23, minute = 59, second = 0, microsecond = 0)
    first_day = last_day.replace(day = 1)
    first_day = first_day.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    return {'first': first_day, 'last': last_day}

def first_last_day_of_week(any_day_of_week):

    '''returns first and last day of quartal by any day of this week as dictionary'''
    last_day = any_day_of_week + timedelta(days=(6 - datetime.now().weekday()))
    last_day = last_day.replace(hour=23, minute=59, second=0, microsecond=0)
    first_day = last_day - timedelta(days=6)
    first_day = first_day.replace(hour=0, minute=0, second=0, microsecond=0)

    return {'first': first_day, 'last': last_day}

def first_last_day_of_quartal(any_day):

    '''returns first and last day of quartal by any day of this quartal as dictionary'''
    if any_day.month <= 3:
        last_day = datetime.now().replace(month=3, day=31, hour=23, minute=59, second=0, microsecond=0)
        first_day = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    elif any_day.month <= 6:
        last_day = datetime.now().replace(month=6, day=30, hour=23, minute=59, second=0, microsecond=0)
        first_day = datetime.now().replace(month=4, day=1, hour=0, minute=0, second=0, microsecond=0)

    elif any_day.month <= 9:
        last_day = datetime.now().replace(month=9, day=30, hour=23, minute=59, second=0, microsecond=0)
        first_day = datetime.now().replace(month=7, day=1, hour=0, minute=0, second=0, microsecond=0)

    elif any_day.month <= 12:
        last_day = datetime.now().replace(month=12, day=31, hour=23, minute=59, second=0, microsecond=0)
        first_day = datetime.now().replace(month=10, day=1, hour=0, minute=0, second=0, microsecond=0)

    return {'first': first_day, 'last': last_day}

def first_last_day_of_half_year(any_day):

    '''returns first and last day of quartal by any day of this half_year as dictionary'''

    if any_day.month <= 6:
        last_day = datetime.now().replace(month=6, day=30, hour=23, minute=59, second=0, microsecond=0)
        first_day = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    else:
        last_day = datetime.now().replace(month=12, day=31, hour=23, minute=59, second=0, microsecond=0)
        first_day = datetime.now().replace(month=7, day=1, hour=0, minute=0, second=0, microsecond=0)

    return {'first': first_day, 'last': last_day}

def first_last_day_of_year(any_day):

    '''returns first and last day of quartal by any day of this year as dictionary'''

    last_day = any_day.replace(month=12, day=31, hour=23, minute=59, second=0, microsecond=0)
    first_day = any_day.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    return {'first': first_day, 'last': last_day}

def get_yesterday(today):

    '''returns yesterday 23:59:59 datetime'''
    yesterday = today - timedelta(days=1)
    return yesterday.replace(hour=23, minute=59, second=0, microsecond=0)

print(first_last_day_of_year(datetime.now()))
print(get_yesterday(datetime.now()))



