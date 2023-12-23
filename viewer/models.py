from django.db import models
from django.db.models import Model, CharField, IntegerField, DateField, ForeignKey, DO_NOTHING, TextField, CASCADE, \
    DecimalField, ImageField, SET_NULL, DateTimeField
from django.contrib.auth.models import User


# Create your models here.


class City(Model):
    name = CharField(max_length=132, null=False, blank=False, unique=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name}"


class Country(Model):
    name = CharField(max_length=132, null=False, blank=False, unique=True)
    city = ForeignKey(City, on_delete=DO_NOTHING, related_name='city_of_country')

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name}"


class Continent(Model):
    name = CharField(max_length=64, null=False, blank=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Hotel(Model):
    name = CharField(max_length=132, null=False, blank=False)
    city = ForeignKey(City, on_delete=DO_NOTHING, related_name='hotels_of_cities')
    star_rating = IntegerField(default=0, choices=[
        (1, '1 hvězdička'),
        (2, '2 hvězdičky'),
        (3, '3 hvězdičky'),
        (4, '4 hvězdičky'),
        (5, '5 hvězdiček'),
    ])
    description = TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class MealPlan(Model):
    name = CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return self.name


class TravelPackage(Model):
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING)
    meal_plan = ForeignKey(MealPlan, on_delete=DO_NOTHING)
    arrival_date = DateField(null=True, blank=True)
    departure_date = DateField(null=True, blank=True)
    price_per_person = DecimalField(max_digits=10, decimal_places=2)
    price_per_child = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.hotel.name} - {self.meal_plan.name}"


class Airport(Model):
    name = CharField(max_length=132, null=True, blank=True)
    airport_city = ForeignKey(City, on_delete=DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.airport_city}"


class Purchase(Model):
    travel_package = ForeignKey(TravelPackage, on_delete=DO_NOTHING)
    customer = ForeignKey(User, on_delete=CASCADE)
    number_of_adults = IntegerField(null=False, blank=False, default=0)
    number_of_children = IntegerField(null=True, blank=True)
    total_price = DecimalField(max_digits=10, decimal_places=2)
    special_requirements = TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer}- {self.travel_package}"


class Images(Model):
    image = ImageField(upload_to='images/')
    description = CharField(max_length=64, null=True, blank=True)
    continent = ForeignKey(Continent, on_delete=DO_NOTHING, null=True, blank=True)
    city = ForeignKey(City, on_delete=DO_NOTHING, null=True, blank=True)
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.description


class Rating(Model):
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    rating = IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.hotel}: {self.rating} od {self.user}"


class Comment (Model):
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    comment = TextField(null=False, blank=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hotel} ({self.user}): {self.comment[:50]}"
