from datetime import timedelta, datetime

from _decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models, transaction
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


class Island(Model):
    name = CharField(max_length=132, null=True, blank=True, verbose_name='Ostrov')
    country = ForeignKey(Country, null=True, blank=True, on_delete=CASCADE, related_name='cities', verbose_name='Stát')

    def __str__(self):
        return f"{self.name} - {self.country}"


class City(Model):
    name = CharField(max_length=132, null=False, blank=False, unique=True, verbose_name='Název')
    country = ForeignKey(Country, null=True, blank=True, on_delete=CASCADE, default=None, verbose_name='Stát')
    island = ForeignKey(Island, null=True, blank=True, on_delete=CASCADE, default=None, related_name='cities',
                        verbose_name='Ostrov')

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name} - {self.country or self.island}"


class Airport(Model):
    name = CharField(max_length=132, null=True, blank=True, verbose_name='Název')
    airport_city = ForeignKey(City, on_delete=CASCADE, null=True, blank=True, verbose_name='Město')

    def __str__(self):
        return f"{self.airport_city} - {self.name}"


class Transportation(Model):
    departure_airport = ForeignKey(Airport, on_delete=CASCADE, null=True, blank=True,
                                   related_name='departure_transportation', verbose_name='Letiště odletu')
    arrival_airport = ForeignKey(Airport, on_delete=CASCADE, null=True, blank=True,
                                 related_name='arrival_transportation', verbose_name='Letiště příletu')
    price = DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Cena dopravy')

    def __str__(self):
        return f"{self.departure_airport} - {self.arrival_airport} : {self.price}"


class Hotel(Model):
    name = CharField(max_length=132, null=False, blank=False, verbose_name='Název')
    city = ForeignKey(City, on_delete=CASCADE, related_name='hotels_of_cities', verbose_name='Město')
    transportation = ForeignKey(Transportation, on_delete=CASCADE, default=None, null=True, blank=True,
                                to_field='id', related_name='transportation_of_hotel', verbose_name='Doprava')
    country = ForeignKey(Country, on_delete=CASCADE, null=True, blank=True, related_name='city_of_country',
                         verbose_name='Stát')
    single_rooms = IntegerField(default=0, verbose_name='Jednolůžkové pokoje')
    double_rooms = IntegerField(default=0, verbose_name='Dvoulůžkové pokoje')
    family_rooms = IntegerField(default=0, verbose_name='Rodinné pokoje')
    suite_rooms = IntegerField(default=0, verbose_name='Apartmány')
    travelers = IntegerField(default=1, verbose_name='Celkem cestujících')
    current_price = DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Aktuální cena')
    total_price = DecimalField(max_digits=10, null=True, blank=True, decimal_places=2, default=0,
                               verbose_name='Cena celkem')

    star_rating = IntegerField(default=0, verbose_name='Počet hvězdiček', choices=[
        (1, '1 hvězdička'),
        (2, '2 hvězdičky'),
        (3, '3 hvězdičky'),
        (4, '4 hvězdičky'),
        (5, '5 hvězdiček'),
    ])
    description = TextField(null=True, blank=True, verbose_name='Popis')
    images = MultiFileField(min_num=1, max_num=6, max_file_size=1024 * 1024 * 5, required=False)

    def get_available_rooms(self, room_type, quantity, arrival_date, departure_date):
        arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d')
        departure_date = datetime.strptime(departure_date, '%Y-%m-%d')
        day = arrival_date

        hotel_single = []
        hotel_double = []
        hotel_family = []
        hotel_suite = []

        while day < departure_date:
            purchases = Purchase.objects.filter(arrival_date__lt=day, departure_date__gt=day)
            day = day + timedelta(days=1)

            number_single = self.single_rooms
            number_double = self.double_rooms
            number_family = self.family_rooms
            number_suite = self.suite_rooms

            for purchase in purchases:
                number_single -= purchase.single_rooms
                number_double -= purchase.double_rooms
                number_family -= purchase.family_rooms
                number_suite -= purchase.suite_rooms
            hotel_single.append(number_single)
            hotel_double.append(number_double)
            hotel_family.append(number_family)
            hotel_suite.append(number_suite)

        if room_type == 'single':
            return min(hotel_single) >= quantity
        elif room_type == 'double':
            return min(hotel_double) >= quantity
        elif room_type == 'family':
            return min(hotel_family) >= quantity
        elif room_type == 'suite':
            return min(hotel_suite) >= quantity
        elif room_type == 'all':
            return {
                'available_rooms': {
                    'single_rooms': min(hotel_single),
                    'double_rooms': min(hotel_double),
                    'family_rooms': min(hotel_family),
                    'suite_rooms': min(hotel_suite)}
            }
        else:
            return False

    def get_images(self):
        return HotelImage.objects.filter(hotel=self)

    def __str__(self):
        return f"{self.name} - Cena bez stravy na týden již od: {self.current_price} Kč"


class MealPlan(Model):
    name = CharField(max_length=32, null=False, blank=False, verbose_name='Název')
    price = DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Cena za stravu')

    def __str__(self):
        return f"{self.name}, {self.price}"


class Traveler(Model):

    first_name = CharField(null=True, blank=True, default=None, max_length=68, verbose_name='Jméno')
    last_name = CharField(null=True, blank=True, default=None, max_length=68, verbose_name='Příjmení')
    birth_date = DateField(null=True, blank=True, default=None, verbose_name='Datum narození')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Purchase(Model):
    traveler = ManyToManyField(Traveler, default=None, null=True, blank=True,
                               related_name='purchase_travelers')
    hotel = ForeignKey(Hotel, on_delete=CASCADE, default=None, null=True, blank=True, related_name='purchase_hotel')
    customer = ForeignKey(User, on_delete=CASCADE, related_name='purchase_customer', verbose_name='Zákazník')
    arrival_date = DateField(null=True, blank=True, verbose_name='Datum příjezdu')
    departure_date = DateField(null=True, blank=True, verbose_name='Datum odjezdu')
    meal_plan = ForeignKey(MealPlan, on_delete=CASCADE, default=None, null=True, blank=True,
                           related_name='travel_packages', verbose_name='Strava')

    single_rooms = IntegerField(null=False, blank=False, default=0,
                                          verbose_name='Počet jednolůžkových pokojů')
    double_rooms = IntegerField(null=False, blank=False, default=0, verbose_name='Počet dvoulůžkových pokojů')
    family_rooms = IntegerField(null=False, blank=False, default=0, verbose_name='Počet rodinných pokojů')
    suite_rooms = IntegerField(null=False, blank=False, default=0, verbose_name='Počet apartmánů')
    total_price = DecimalField(max_digits=10, null=True, blank=True, decimal_places=2, default=0,
                               verbose_name='Cena celkem')
    transportation = ForeignKey(Transportation, on_delete=CASCADE, default=None, null=True, blank=True,
                                related_name='purchase_transportation', verbose_name='Doprava')
    travelers = IntegerField(default=1, verbose_name='Celkem cestujících')
    special_requirements = TextField(null=True, blank=True, verbose_name='Zvláštní požadavky')

    def save(self, *args, **kwargs):
        if not self.pk:
            hotel = Hotel.objects.get(pk=self.hotel.pk)
            if (
                hotel.get_available_rooms('single', self.single_rooms, self.arrival_date, self.departure_date) and
                hotel.get_available_rooms('double', self.double_rooms, self.arrival_date, self.departure_date) and
                hotel.get_available_rooms('family', self.family_rooms, self.arrival_date, self.departure_date) and
                hotel.get_available_rooms('suite', self.suite_rooms, self.arrival_date, self.departure_date)
            ):
                super().save(*args, **kwargs)
            else:
                raise ValueError("Nedostatek volných pokojů pro dané období.")
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer}- {self.total_price}"


class Prices(Model):
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING)
    arrival_date = DateField(null=True, blank=True, verbose_name='Datum příjezdu')
    departure_date = DateField(null=True, blank=True, verbose_name='Datum odjezdu')
    price_single_room = DecimalField(max_digits=10, null=True, blank=True, decimal_places=2, default=0,
                                     verbose_name='Cena za jednolůžkový pokoj')
    price_double_room = DecimalField(max_digits=10, null=True, blank=True, decimal_places=2, default=0,
                                     verbose_name='Cena za dvoulůžkový pokoj')
    price_family_room = DecimalField(max_digits=10, null=True, blank=True, decimal_places=2, default=0,
                                     verbose_name='Cena za rodinný pokoj')
    price_suite = DecimalField(max_digits=10, null=True, blank=True, decimal_places=2, default=0,
                               verbose_name='Cena za apartmán')

    def __str__(self):
        return f"{self.hotel.name} - {self.arrival_date} to {self.departure_date}"


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
