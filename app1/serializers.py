from rest_framework import serializers
from app1.models import Service_CI, Staff

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        #fields = ('id', 'name')

class Service_CI_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Service_CI
        #fields = ('id', 'name')
