from django import template
from app1.models import Metric, MetricValue


register = template.Library()

@register.simple_tag
def get_link(object, request):
    if type(object) is Metric:
        return request.build_absolute_uri('/admin/app1/metric/') + str(object.id) + "/change"
    elif type(object) is MetricValue:
        return request.build_absolute_uri('/admin/app1/metricvalue/') + str(object.id) + "/change"


@register.simple_tag
def add_another_link(object, request):
    if type(object) is Metric:
        return request.build_absolute_uri('/admin/app1/metric/add')
    elif type(object) is MetricValue:
        return request.build_absolute_uri('/admin/app1/metricvalue/add')

@register.simple_tag
def add_another_text(object):
    if type(object) is Metric:
        return "Add another Metric"
    elif type(object) is MetricValue:
        return "Add another Metric value"

@register.simple_tag
def get_obj(objects):
    return objects[0].original

@register.simple_tag
def define(val=None):
  return val

