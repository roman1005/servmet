from django import template
from app1.models import Metric, MetricValue

register = template.Library()

@register.simple_tag
def get_link(object):
    if type(object) is Metric:
        return "http://127.0.0.1:8000/admin/app1/metric/" + str(object.id) + "/change"
    elif type(object) is MetricValue:
        return "http://127.0.0.1:8000/admin/app1/metricvalue/" + str(object.id) + "/change"
