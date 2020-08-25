from django import template
from app1.models import SubPortfolio, Service, Metric, MetricValue


register = template.Library()

@register.simple_tag
def get_metric_link(original, request):
    return request.build_absolute_uri('/admin/app1/metric/') + str(original.metric.id) + "/change"

@register.simple_tag
def get_link(object, request):
    if type(object) is SubPortfolio:
        return request.build_absolute_uri('/admin/app1/subportfolio/') + str(object.id) + "/change"
    elif type(object) is Service:
        return request.build_absolute_uri('/admin/app1/service/') + str(object.id) + "/change"
    elif type(object) is Metric:
        return request.build_absolute_uri('/admin/app1/metric/') + str(object.id) + "/change"
    elif type(object) is MetricValue:
        return request.build_absolute_uri('/admin/app1/metricvalue/') + str(object.id) + "/change"

@register.simple_tag
def get_service_link(original, request):
  id = original.service_id
  return request.build_absolute_uri('/admin/app1/service/') + str(id) + "/change"

@register.simple_tag
def get_subport_link(original, request):
    id = original.subportfolio_id
    return request.build_absolute_uri('/admin/app1/subportfolio/') + str(id) + "/change"

@register.simple_tag
def get_port_link(original, request):
    id = original.portfolio_id
    return request.build_absolute_uri('/admin/app1/portfolio/') + str(id) + "/change"

@register.simple_tag
def get_admin_link(request):
    return request.build_absolute_uri('/admin/')
'''
@register.simple_tag
def define(val=None):
  return val

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
'''


