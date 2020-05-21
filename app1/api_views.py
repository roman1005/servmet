from rest_framework import viewsets
from rest_framework.views import APIView
from . import models
from . import serializers
from .serializers import StaffSerializer
from rest_framework.response import Response
from django.contrib.auth.models import Permission

class StaffView(APIView):

    def get(self, request):
        staff = models.Staff.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = StaffSerializer(staff, many=True)
        for perm in Permission.objects.filter(user=request.user, codename='add_service'):
            print(perm)
        response= Response({"staff": serializer.data})
        return response


class ServiceViewset(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

