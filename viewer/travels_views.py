
from django.shortcuts import render
from .models import Continent, Country


def first_minute(request):
    country_ids = [2, 3, 27, 45, 51]
    continents = Continent.objects.all()
    cities_by_continent = {}

    for continent in continents:
        countries = Country.objects.filter(id__in=country_ids, continent=continent)
        cities = []
        for country in countries:
            cities.extend(country.city_set.all())
        cities_by_continent[continent.name] = cities

    return render(request, 'first_minute.html', {'cities_by_continent': cities_by_continent})


def last_minute(request):
    country_ids = [38, 43, 71, 5]
    continents = Continent.objects.all()
    cities_by_continent = {}

    for continent in continents:
        countries = Country.objects.filter(id__in=country_ids, continent=continent)
        cities = []
        for country in countries:
            cities.extend(country.city_set.all())
        cities_by_continent[continent.name] = cities

    return render(request, 'last_minute.html', {'cities_by_continent': cities_by_continent})
