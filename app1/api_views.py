from rest_framework import viewsets
from rest_framework.views import APIView
from . import models
from . import serializers
from .serializers import StaffSerializer,ServiceSerializer
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission, User
from django.shortcuts import get_object_or_404
from .models import Staff, Service
from django.http import JsonResponse
from rest_framework import status


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
        # Create an article from the above data
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            req_owner = Staff.objects.get(pk = request.data['owner'])
            req_customer = Staff.objects.get(pk = request.data['customer'])
            serializer.save(owner = req_owner, customer = req_customer)

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


class ServiceViewset(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

