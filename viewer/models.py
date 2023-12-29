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


class Hotel(Model):
    name = CharField(max_length=132, null=False, blank=False, verbose_name='Název')
    city = ForeignKey(City, on_delete=DO_NOTHING, related_name='hotels_of_cities', verbose_name='Město')
    star_rating = IntegerField(default=0, verbose_name='Počet hvězdiček', choices=[
        (1, '1 hvězdička'),
        (2, '2 hvězdičky'),
        (3, '3 hvězdičky'),
        (4, '4 hvězdičky'),
        (5, '5 hvězdiček'),
    ])
    description = TextField(null=True, blank=True, verbose_name='Popis')
    images = MultiFileField(min_num=1, max_num=6, max_file_size=1024 * 1024 * 5, required=False)

    def get_images(self):
        return HotelImage.objects.filter(hotel=self)

    def __str__(self):
        return self.name


class MealPlan(Model):
    name = CharField(max_length=32, null=False, blank=False, verbose_name='Název')

    def __str__(self):
        return self.name


class TravelPackage(Model):
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING)
    meal_plan = ForeignKey(MealPlan, on_delete=DO_NOTHING, verbose_name='Strava')
    arrival_date = DateField(null=True, blank=True, verbose_name='Datum příjezdu')
    departure_date = DateField(null=True, blank=True, verbose_name='Datum odjezdu')
    price_per_person = DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena za osobu')
    price_per_child = DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena za dítě')

    def __str__(self):
        return f"{self.hotel.name} - {self.meal_plan.name}"


class Airport(Model):
    name = CharField(max_length=132, null=True, blank=True, verbose_name='Název')
    airport_city = ForeignKey(City, on_delete=DO_NOTHING, null=True, blank=True, verbose_name='Město')

    def __str__(self):
        return f"{self.name} - {self.airport_city}"


class Purchase(Model):
    travel_package = ForeignKey(TravelPackage, on_delete=DO_NOTHING, verbose_name='Cestovní balíček')
    customer = ForeignKey(User, on_delete=CASCADE, verbose_name='Zákazník')
    number_of_adults = IntegerField(null=False, blank=False, default=0, verbose_name='Počet dospělých')
    number_of_children = IntegerField(null=True, blank=True, verbose_name='Počet dětí')
    total_price = DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena celkem')
    special_requirements = TextField(null=True, blank=True, verbose_name='Zvláštní požadavky')

    def __str__(self):
        return f"{self.customer}- {self.travel_package}"


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
