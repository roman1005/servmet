from rest_framework import viewsets
from rest_framework.views import APIView
from . import models
from . import serializers
from .serializers import StaffSerializer,ServiceSerializer, MetricSerializer, MetricValueSerializer
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Staff, Service, Metric, MetricValue
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist

class StaffView(APIView):

    def get(self, request):
        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.view_staff'):
            raise PermissionDenied()

        staff = models.Staff.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = StaffSerializer(staff, many=True)


        response= Response({"staff": serializer.data})
        return response


class ServiceView(APIView):

    def get(self, request):
        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.view_service'):
            raise PermissionDenied()

        service = models.Service.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = ServiceSerializer(service, many=True)

        response = Response({"services": serializer.data})
        return response

    def post(self, request):

        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.add_service'):
            raise PermissionDenied()

        #service = request.data.get('service')
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            to_post = True

            try:
                req_owner = Staff.objects.get(pk=request.data['owner'])
            except KeyError:
                to_post = False
                return JsonResponse({"owner": ["This field is required."]})
            except ObjectDoesNotExist:
                return JsonResponse({"owner": ["Owner with such id does not exist."]})

            try:
                req_customer = Staff.objects.get(pk=request.data['customer'])
            except KeyError:
                to_post = False
                return JsonResponse({"customer": ["This field is required."]})
            except ObjectDoesNotExist:
                return JsonResponse({"customer": ["Customer with such id does not exist."]})

            if to_post:

                serializer.save(owner=req_owner, customer=req_customer)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = User.objects.get(username=request.user)
        if not user.has_perm('app1.delete_service'):
            raise PermissionDenied()
        service = Service.objects.get(pk=pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):

        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.add_service'):
            raise PermissionDenied()

        saved_article = get_object_or_404(Service.objects.all(), id=pk)
        data = request.data.get('service')
        serializer = ServiceSerializer(instance=saved_article, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            service_saved = serializer.save()
        return Response({
            "success": "Service '{}' updated successfully".format(service_saved.service_name)
        })


class MetricView(APIView):

    def get(self, request):
        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.view_metric'):
            raise PermissionDenied()

        metric = models.Metric.objects.all()

        serializer = MetricSerializer(metric, many=True)

        response = Response({"metrics": serializer.data})
        return response

    def post(self, request):

        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.add_metric'):
            raise PermissionDenied()

        serializer = MetricSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            try:
                req_service = Service.objects.get(pk=request.data['service'])
                serializer.save(metric=req_service)

                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

            except KeyError:
                return JsonResponse({"service": ["This field is required."]})

            except ObjectDoesNotExist:
                return JsonResponse({"service": ["Service with such id does not exist."]})

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

class MetricValueView(APIView):

    def get(self, request):
        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.view_metricvalue'):
            raise PermissionDenied()

        metric_value = models.MetricValue.objects.all()
        serializer = MetricValueSerializer(metric_value, many=True)

        response = Response({"metricvalues": serializer.data})
        return response

    def post(self, request):

        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.add_metricvalue'):
            raise PermissionDenied()


        serializer = MetricValueSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            try:
                #later when unique change filter for get
                req_metric = Metric.objects.filter(mtrc_design_id=request.data['mtrc_design_id'])[0]
                #req_metric = Metric.objects.get(mtrc_design_id=request.data['mtrc_design_id'])
                serializer.save(metric = req_metric)

                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

            except KeyError:
                return JsonResponse({"mtrc_design_id": ["This field is required."]})

            #later change IndexError for ObjectDoesNotExist
            except IndexError:
                return JsonResponse({"mtrc_design_id": ["Metric with such mtrc_design_id does not exist."]})
            '''
            except ObjectDoesNotExist:
                return JsonResponse({"mtrc_design_id": ["Metric with such mtrc_design_id does not exist."]})
            '''


        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceViewset(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer



