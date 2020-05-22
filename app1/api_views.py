from rest_framework import viewsets
from rest_framework.views import APIView
from . import models
from . import serializers
from .serializers import StaffSerializer,ServiceSerializer
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission, User
from django.shortcuts import get_object_or_404


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

        service = request.data.get('service')
        # Create an article from the above data
        serializer = ServiceSerializer(data=service)
        if serializer.is_valid(raise_exception=True):
            service_saved = serializer.save()
        return Response({"success": "Service '{}' created successfully".format(service_saved.service_name )})

class ServiceViewset(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

