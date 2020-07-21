from django.test import TestCase
from datetime import datetime, timedelta
from .models import MetricValueRegistration

now = datetime.now()
now = now.replace(day = 26)
date_begin = now - timedelta(days=now.weekday(), weeks=0)
date_begin = date_begin.replace(hour=0, minute=0, second=0, microsecond=0)
print(date_begin)
# Create your tests here.
