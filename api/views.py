from rest_framework import mixins, generics
from django.shortcuts import render
from rest_framework.response import Response

from api.serializers import *
from viewer.models import TravelPackage


# Create your views here.

class TravelPackages(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = TravelPackage.objects.all()
    serializer_class = TravelPackageSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PricesAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Prices.objects.all()
    serializer_class = PricesSerializer

    def get(self, request, *args, **kwargs):
        hotel_id = self.kwargs.get('pk')
        prices = Prices.objects.filter(hotel=hotel_id)
        serializer = self.serializer_class(prices, many=True)
        return Response(serializer.data)


class TransportationAPI(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MealPlanAPI(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
