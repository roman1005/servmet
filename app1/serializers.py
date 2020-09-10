from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from app1.models import *

'''
class MakeActive:
    def set_active(self, foo):
        return False
'''

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class StaffSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)



class SubPortfolioSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPortfolio
        exclude = []


class PortfolioSerializer(serializers.ModelSerializer):
    #subportfolio_set = SubPortfolioSetSerializer(many=True)
    #active = serializers.SerializerMethodField('set_active')
    class Meta:
        model = Portfolio
        exclude = []
        depth = 0


class ServiceSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = []
        depth = 0

class ServiceSerializer(serializers.ModelSerializer):

    #active = serializers.SerializerMethodField('set_active')
    #current = serializers.SerializerMethodField('set_active')
    class Meta:
        model = Service
        #fields = ('service_name',)
        exclude = []
        depth = 0

    '''
    def update(self, instance, validated_data):
        instance.service_name = validated_data.get('service_name', instance.service_name)
        instance.portfolio = validated_data.get('portfolio', instance.portfolio)
        instance.sub_portfolio = validated_data.get('sub_portfolio', instance.sub_portfolio)
        instance.design_id = validated_data.get('design_id', instance.design_id)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
    '''

class SubPortfolioSerializer(serializers.ModelSerializer):
    #services= SerializerMethodField()
    #active = serializers.SerializerMethodField('set_active')

    class Meta:
        model = SubPortfolio
        exclude = []
        depth = 0

    def get_services(self, obj: SubPortfolio):
        services=Service.objects.filter(subportfolio_id=obj.id)
        serializer=ServiceSetSerializer(services,many=True)
        return serializer.data

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        depth = 2
        exclude = []


class MetricValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricValue
        depth = 1
        exclude = []
