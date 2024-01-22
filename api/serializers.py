from rest_framework import serializers

from viewer.models import Prices, Transportation, MealPlan


class PricesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prices
        fields = '__all__'


class TransportationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transportation
        fields = '__all__'


class MealPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = MealPlan
        fields = '__all__'

