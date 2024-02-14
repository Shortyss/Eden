from rest_framework import serializers
from rest_framework.response import Response

from viewer.models import Prices, Transportation, MealPlan, Hotel, Purchase


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


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = '__all__'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        arrival_date = self.request.query_params.get('arrival_date')
        departure_date = self.request.query_params.get('departure_date')

        if arrival_date and departure_date:
            serializer = self.get_serializer(instance,
                                             context={'arrival_date': arrival_date, 'departure_date': departure_date})
            return Response(serializer.data)
        else:
            return super().get(request, *args, **kwargs)


class HotelCustomSerializer(serializers.Serializer):
    def get(self, request, pk, *args, **kwargs):
        hotel = Hotel.objects.get(id=pk)
        instance = self.get_object()
        arrival_date = self.request.query_params.get('arrival_date')
        departure_date = self.request.query_params.get('departure_date')
        print('API')

        if arrival_date and departure_date:
            context = hotel.get_available_rooms(room_type=all, quantity=0, arrival_date=arrival_date,
                                                departure_date=departure_date)
            serializer = self.get_serializer(instance,
                                             context=context)
            return Response(serializer.data)
        else:
            return super().get(request, *args, **kwargs)


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = '__all__'
