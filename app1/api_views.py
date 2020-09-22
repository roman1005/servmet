from rest_framework import viewsets
from rest_framework.views import APIView
from . import models
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from .serializers import *
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Portfolio, SubPortfolio, Staff, Service, Metric, MetricValue
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
import datetime as dt
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta

class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

class UserViewSet(APIView):
    """
    Provides basic CRUD functions for the User model
    """
    permission_classes = (ReadOnly,)
    def get(self, reqest):
        queryset = User.objects.all()
        users = UserSerializer(queryset, many=True)
        response = Response({"users": users.data})
        return response


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

class PortfolioView(APIView):

    def get(self, request):
        if request.user.id is not None:
            user = User.objects.get(username=request.user)
        elif 'token' in request.query_params.keys():
            try:
                data = {'token': request.query_params['token']}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                request.user = user
            except ValidationError as v:
                return HttpResponse('Failed to authorize the user.')
                # print("validation error", v)
        else:
            return HttpResponse('Failed to authorize the user.')
        if not user.has_perm('app1.view_portfolio'):
            raise PermissionDenied()

        portfolio = Portfolio.objects.all().order_by('order')
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = PortfolioSerializer(portfolio, many=True)

        response = Response({"portfolios": serializer.data})

        return response


class SubPortfolioView(APIView):

    def get(self, request):
        if request.user.id is not None:
            user = User.objects.get(username=request.user)
        elif 'token' in request.query_params.keys():
            try:
                data = {'token': request.query_params['token']}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                request.user = user
            except ValidationError as v:
                return HttpResponse('Failed to authorize the user.')
                # print("validation error", v)
        else:
            return HttpResponse('Failed to authorize the user.')
        if not user.has_perm('app1.view_subportfolio'):
            raise PermissionDenied()

        sub_portfolio = SubPortfolio.objects.all().order_by('portfolio__order','order')
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = SubPortfolioSerializer(sub_portfolio, many=True)

        response = Response({"subportfolios": serializer.data})
        return response

class SubPortService(APIView):

    def get(self, request, subportfolio):
        
        if request.user.id is not None:
            user = User.objects.get(username=request.user)
        elif 'token' in request.query_params.keys():
            try:
                data = {'token': request.query_params['token']}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                request.user = user
            except ValidationError as v:
                return HttpResponse('Failed to authorize the user.')
                #print("validation error", v)
        else:
            return HttpResponse('Failed to authorize the user.')

        subport_id = SubPortfolio.objects.get(name=subportfolio).id
        services = Service.objects.filter(subportfolio_id=subport_id)
        serializer = ServiceSerializer(services, many=True)

        response = Response({"services": serializer.data})
        return response

'''
class SubPortService(APIView):

    def get(self, request, subportfolio):

        if request.user.id is not None:
            user = User.objects.get(username=request.user)
        elif 'token' in request.query_params.keys():
            try:
                data = {'token': request.query_params['token']}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                request.user = user
            except ValidationError as v:
                return HttpResponse('Failed to authorize the user.')
                # print("validation error", v)
        else:
            return HttpResponse('Failed to authorize the user.')

        subport_id = SubPortfolio.objects.get(name=subportfolio).id
        services = Service.objects.filter(subportfolio_id=subport_id)
        serializer = ServiceSerializer(services, many=True)

        response = Response({"services": serializer.data})
        return response
'''

class PortSubPort(APIView):

    def get(self, request, portfolio):

        if request.user.id is not None:
            user = User.objects.get(username=request.user)
        elif 'token' in request.query_params.keys():
            try:
                data = {'token': request.query_params['token']}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                request.user = user
            except ValidationError as v:
                return HttpResponse('Failed to authorize the user.')
                # print("validation error", v)
        else:
            return HttpResponse('Failed to authorize the user.')

        port_id = Portfolio.objects.get(name=portfolio).id
        services = SubPortfolio.objects.filter(portfolio_id=port_id)
        serializer = SubPortfolioSerializer(services, many=True)

        response = Response({"subportfolios": serializer.data})
        return response


class ServiceView(APIView):

    def get(self, request):
        if request.user.id is not None:
            user = User.objects.get(username=request.user)
        elif 'token' in request.query_params.keys():
            try:
                data = {'token': request.query_params['token']}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                request.user = user
            except ValidationError as v:
                return HttpResponse('Failed to authorize the user.')
                #print("validation error", v)
        else:
            return HttpResponse('Failed to authorize the user.')
        if not user.has_perm('app1.view_service'):
            raise PermissionDenied()

        #subport_id = SubPortfolio.objects.get(name="Basic TelCo").id
        #service = Service.objects.filter(subportfolio_id = subport_id)
        # the many param informs the serializer that it will be serializing more than a single article.
        service = Service.objects.all()
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
                return JsonResponse({"owner": ["This field is required."]},status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return JsonResponse({"owner": ["Owner with such id does not exist."]},status=status.HTTP_200_OK)

            try:
                req_customer = Staff.objects.get(pk=request.data['customer'])
            except KeyError:
                to_post = False
                return JsonResponse({"customer": ["This field is required."]},status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return JsonResponse({"customer": ["Customer with such id does not exist."]},status=status.HTTP_200_OK)

            if to_post:

                serializer.save(owner=req_owner, customer=req_customer)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_200_OK)

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
                return JsonResponse({"service": ["This field is required."]},status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return JsonResponse({"service": ["Service with such id does not exist."]},status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_200_OK)

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

class MetricValueView(APIView):

    def get(self, request):

        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.view_metricvalue'):
            raise PermissionDenied()

        if 'design_id' in request.data.keys():
            try:
                metric = Metric.objects.get(design_id=request.data['design_id'])
                metric_value = MetricValue.objects.filter(metric=metric)
            except ObjectDoesNotExist:
                return JsonResponse({"design_id": ["Metric with such design_id does not exist."]}, status=status.HTTP_200_OK)
            except ValueError:
                return JsonResponse(
                    {'design_id': ["Expected a number but got '" + str(request.data['design_id']) + "'"]}, status=status.HTTP_200_OK)

            serializer = MetricValueSerializer(metric_value, many=True)

            response = Response({"metricvalues": serializer.data})
            return response

        else:
            return JsonResponse({"design_id": ["This field is required."]},status=status.HTTP_200_OK)

    def post(self, request):

        user = User.objects.get(username=request.user)

        if not user.has_perm('app1.add_metricvalue'):
            raise PermissionDenied()

        if 'period' in request.data.keys():
            if 'date_begin' in request.data.keys() or 'date_end' in request.data.keys():
                return JsonResponse({"Fields required": ["Either begin and end date or period should be passed."]},status=status.HTTP_200_OK)

            else:
                day = datetime.now()
                if request.data['period'] == 'last_week':
                    day=day- timedelta( weeks=1)
                    period = first_last_day_of_week(day)
                elif request.data['period']  == 'last_month':
                    day=day -relativedelta(months=1)
                    period = first_last_day_of_month(day)
                elif request.data['period'] == 'last_quarter':
                    day = day - relativedelta(months=3)
                    period = first_last_day_of_quartal(day)
                elif request.data['period'] == 'last_half-year':
                    day = day - relativedelta(months=6)
                    period = first_last_day_of_half_year(day)
                elif request.data['period'] == 'last_year':
                    day = day - relativedelta(months=12)
                    period = first_last_day_of_year(day)
                else:
                    return JsonResponse({"period": ["Incorrect value. Valid are the following: 'last_week', 'last_month','last_quarter',''last_half-year'' "]},status=status.HTTP_200_OK)
                request.data['date_begin'] = period["first"]
                request.data['date_end']= period["last"]



        elif not ('date_begin' in request.data.keys() or 'date_end' in request.data.keys()):
            return JsonResponse({"Fields required": ["Either period or date_begin and date_end fields are required."]},status=status.HTTP_200_OK)


        serializer = MetricValueSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            try:
                req_metric = Metric.objects.get(design_id=request.data['design_id'])
                instance=serializer.save(metric = req_metric)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

            except KeyError:
                return JsonResponse({"design_id": ["This field is required."]}, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return JsonResponse({"design_id": ["Metric with such design_id does not exist."]}, status=status.HTTP_200_OK)

            except ValueError:
                return JsonResponse({'design_id': ["Expected a number but got '" + str(request.data['design_id']) + "'"]}, status=status.HTTP_200_OK)

            except IntegrityError:
                return HttpResponse('Duplicate entry: "metric", "date_begin", "date_end" should be unique combination of fields.')

            except ValidationError as err:
                return HttpResponse(err.__str__(), status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_200_OK)

        #except KeyError:
            #return JsonResponse("design_id: This field is required." + serializer.errors, status=status.HTTP_200_OK)


class ServiceViewset(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer



