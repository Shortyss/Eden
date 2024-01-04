from _decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model, CharField, IntegerField, DateField, ForeignKey, DO_NOTHING, TextField, CASCADE, \
    DecimalField, ImageField, SET_NULL, DateTimeField, ManyToManyField
from django.contrib.auth.models import User
from multiupload.fields import MultiFileField


# Create your models here.


class Continent(Model):
    name = CharField(max_length=64, null=False, blank=False, unique=True, verbose_name='Název')

    def __str__(self):
        return f"{self.name}"


class Country(Model):
    name = CharField(max_length=132, null=False, blank=False, unique=True, verbose_name='Název')
    continent = ForeignKey(Continent, null=True, blank=True, on_delete=CASCADE, default=None, verbose_name='Kontinent')

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name}"


class City(Model):
    name = CharField(max_length=132, null=False, blank=False, unique=True, verbose_name='Název')
    country = ForeignKey(Country, null=True, blank=True, on_delete=CASCADE, default=None, verbose_name='Stát')

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name}"


class Airport(Model):
    name = CharField(max_length=132, null=True, blank=True, verbose_name='Název')
    airport_city = ForeignKey(City, on_delete=DO_NOTHING, null=True, blank=True, verbose_name='Město')

    def __str__(self):
        return f"{self.name} - {self.airport_city}"


class Hotel(Model):
    name = CharField(max_length=132, null=False, blank=False, verbose_name='Název')
    city = ForeignKey(City, on_delete=DO_NOTHING, related_name='hotels_of_cities', verbose_name='Město')
    country = ForeignKey(Country, on_delete=DO_NOTHING, null=True, blank=True, related_name='city_of_country', verbose_name='Stát')
    airport = ForeignKey(Airport, on_delete=DO_NOTHING, null=True, blank=True, related_name='hotel_airport', verbose_name='Letiště')

    total_rooms = IntegerField(default=0, verbose_name='Celkový počet pokojů')
    booked_rooms = IntegerField(default=0, verbose_name='Rezervované pokoje')
    single_rooms = IntegerField(default=0, verbose_name='Jednolůžkové pokoje')
    double_rooms = IntegerField(default=0, verbose_name='Dvoulůžkové pokoje')
    family_rooms = IntegerField(default=0, verbose_name='Rodinné pokoje')
    suites = IntegerField(default=0, verbose_name='Apartmány')

    star_rating = IntegerField(default=0, verbose_name='Počet hvězdiček', choices=[
        (1, '1 hvězdička'),
        (2, '2 hvězdičky'),
        (3, '3 hvězdičky'),
        (4, '4 hvězdičky'),
        (5, '5 hvězdiček'),
    ])
    description = TextField(null=True, blank=True, verbose_name='Popis')
    images = MultiFileField(min_num=1, max_num=6, max_file_size=1024 * 1024 * 5, required=False)

    def available_rooms(self, room_type=None):
        if room_type is None:
            return self.total_rooms - self.booked_rooms
        elif room_type == 'single':
            return self.single_rooms - self.booked_rooms
        elif room_type == 'double':
            return self.double_rooms - self.booked_rooms
        elif room_type == 'family':
            return self.family_rooms - self.booked_rooms
        elif room_type == 'suite':
            return self.suites - self.booked_rooms
        else:
            return 0

    def get_images(self):
        return HotelImage.objects.filter(hotel=self)

    def __str__(self):
        return self.name


class MealPlan(Model):
    name = CharField(max_length=32, null=False, blank=False, verbose_name='Název')
    price = DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Cena za stravu')

    def __str__(self):
        return f"{self.name}, {self.price}"


class Transportation(Model):
    departure_airport = ForeignKey(Airport, on_delete=DO_NOTHING, null=True, blank=True,
                                   related_name='departure_transportation', verbose_name='Letiště odletu')
    arrival_airport = ForeignKey(Airport, on_delete=DO_NOTHING, null=True, blank=True,
                                 related_name='arrival_transportation', verbose_name='Letiště příletu')
    price = DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Cena dopravy')


class TravelPackage(Model):
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING)
    meal_plan = ForeignKey(MealPlan, on_delete=DO_NOTHING, related_name='travel_packages', verbose_name='Strava')
    number_of_adults = IntegerField(null=False, blank=False, default=0, verbose_name='Počet dospělých')
    number_of_children = IntegerField(null=True, blank=True, default=0, verbose_name='Počet dětí')
    transportation = ForeignKey(Transportation, on_delete=DO_NOTHING, null=True, blank=True,
                                related_name='transportation', verbose_name='Doprava')
    arrival_date = DateField(null=True, blank=True, verbose_name='Datum příjezdu')
    departure_date = DateField(null=True, blank=True, verbose_name='Datum odjezdu')
    price_per_day_adult = DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Cena za osobu')
    price_per_day_children = DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Cena za dítě')
    price_modifier = DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Upravená cena')

    def calculate_total_price(self):
        meal_price = self.meal_plan.price
        transport_price = self.transportation.price if self.transportation else 0
        stay = (self.departure_date - self.arrival_date).days

        total_price_per_day_a = meal_price + self.price_per_day_adult + self.price_modifier
        total_price_per_day_ch = meal_price + self.price_per_day_children + self.price_modifier

        total_price = (total_price_per_day_a * self.number_of_adults +
                       total_price_per_day_ch * (self.number_of_children or 0)) * stay

        total_price += transport_price

        return Decimal(total_price)

    def __str__(self):
        return f"{self.hotel.name} - {self.meal_plan.name}"


class Traveler(Model):
    first_name = CharField(null=False, blank=False, max_length=68, verbose_name='Jméno')
    last_name = CharField(null=False, blank=False, max_length=68, verbose_name='Příjmení')
    birth_date = DateField(null=False, blank=False, default=None, verbose_name='Datum narození')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Purchase(Model):
    customer = ForeignKey(User, on_delete=CASCADE, verbose_name='Zákazník')
    total_price = ForeignKey(TravelPackage, on_delete=DO_NOTHING, verbose_name='Cena celkem')
    travelers = ManyToManyField(Traveler, related_name='travelers_purchases', verbose_name='Cestující')
    special_requirements = TextField(null=True, blank=True, verbose_name='Zvláštní požadavky')

    def __str__(self):
        return f"{self.customer}- {self.total_price}"


class HotelImage(Model):
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=DO_NOTHING)
    image = ImageField(upload_to='hotel_images/')
    description = CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.description if self.description else "No description"


class Rating(Model):
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    rating = IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.hotel}: {self.rating} od {self.user}"


class Comment (Model):
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    comment = TextField(null=False, blank=False, verbose_name='Komentář')
    created = DateTimeField(auto_now_add=True, verbose_name='Vytvořeno')
    updated = DateTimeField(auto_now=True, verbose_name='Změněno')

    def __str__(self):
        return f"{self.hotel} ({self.user}): {self.comment[:50]}"
