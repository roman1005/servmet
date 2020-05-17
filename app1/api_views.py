from rest_framework import viewsets
from . import models
from . import serializers

class StaffViewset(viewsets.ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer

class BService_CI_Viewset(viewsets.ModelViewSet):
    queryset = models.Service_CI.objects.all()
    serializer_class = serializers.Service_CI_Serializer

