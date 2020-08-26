from rest_framework import serializers
from app1.models import *

class StaffSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        exclude = []
        depth = 1


class SubPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPortfolio
        exclude = []
        depth = 2

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = []
        depth = 3

    def update(self, instance, validated_data):
        instance.service_name = validated_data.get('service_name', instance.service_name)
        instance.portfolio = validated_data.get('portfolio', instance.portfolio)
        instance.sub_portfolio = validated_data.get('sub_portfolio', instance.sub_portfolio)
        instance.design_id = validated_data.get('design_id', instance.design_id)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance


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
