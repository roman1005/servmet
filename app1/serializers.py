from rest_framework import serializers
from app1.models import Service, Staff

class StaffSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    lastname= serializers.CharField()

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = []
        depth= 1
