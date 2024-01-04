from datetime import datetime
from logging import getLogger

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from viewer.models import *
from django.core.files.base import ContentFile
from django.db.models import Avg, Q
from django.forms import ModelForm, Form, ModelMultipleChoiceField, ChoiceField, Select, inlineformset_factory, \
    CharField, Textarea, ClearableFileInput, FileField, HiddenInput, FileInput, SelectDateWidget, forms, \
    CheckboxSelectMultiple, MultipleChoiceField
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

# Create your views here.
LOGGER = getLogger()


def index(request):
    return render(request, 'index.html')


def administration(request):
    return render(request, 'administration.html', )


# RATING


def rate_hotel(request):
    user = request.user
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel_id')
        hotel_object = Hotel.objects.get(id=hotel_id)
        rating = request.POST.get('rating')

        if rating:
            if Rating.objects.filter(hotel=hotel_object, user=user).count() > 0:
                user_rating = Rating.objects.get(hotel=hotel_object, user=user)
                user_rating.rating = rating
                user_rating.save()
            else:
                Rating.objects.create(
                    hotel=hotel_object,
                    user=user,
                    rating=rating
                )

        return redirect(f"/hotel/{hotel_id}/")


def add_comment(request):
    user = request.user
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel_id')
        hotel_object = Hotel.objects.get(id=hotel_id)
        comment = request.POST.get('comment').strip()
        if comment:
            Comment.objects.create(
                hotel=hotel_object,
                user=user,
                comment=comment
            )

    return redirect(f"/hotel/{hotel_id}")


# CONTINENT


def continent(request, pk):
    continent_object = Continent.objects.get(id=pk)
    countries = Country.objects.filter(continent=continent_object)
    context = {'continent': continent_object, 'countries': countries}
    return render(request, 'continent.html', context)


class ContinentModelForm(ModelForm):

    class Meta:
        model = Continent
        fields = '__all__'

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name'].strip().capitalize()
        return name


class ContinentView(View):
    def get(self, request):
        continent_list = Continent.objects.all()
        context = {'continents': continent_list}
        return render(request, 'continent_admin.html', context)


class ContinentCreateView(CreateView):
    template_name = 'continent_create.html'
    form_class = ContinentModelForm
    success_url = reverse_lazy('administration')


class ContinentCountriesView(View):
    template_name = None

    def get(self, request, pk):
        continent_object = Continent.objects.get(id=pk)
        countries = Country.objects.filter(continent=continent_object)
        return render(request, self.template_name, {'countries': countries})


class EuropeCountriesView(ContinentCountriesView):
    template_name = 'europe.html'


class AsiaCountriesView(ContinentCountriesView):
    template_name = 'asia.html'


class AfricaCountriesView(ContinentCountriesView):
    template_name = 'africa.html'


class AmericaCountriesView(ContinentCountriesView):
    template_name = 'america.html'


class ContinentUpdateView(UpdateView):
    template_name = 'continent_create.html'
    model = Continent
    form_class = ContinentModelForm
    success_url = reverse_lazy('administration')


class ContinentDeleteView(DeleteView):
    template_name = 'continent_confirm_delete.html'
    model = Continent
    success_url = reverse_lazy('administration')


# COUNTRY


def country(request, pk):
    country_object = Country.objects.get(id=pk)
    cities = City.objects.filter(country=country_object)
    context = {'country': country_object, 'cities': cities}
    return render(request, 'country.html', context)


class CountryModelForm(ModelForm):

    class Meta:
        model = Country
        fields = '__all__'

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name'].strip().title()
        return name


class CountryView(View):
    def get(self, request):
        countries_list = Country.objects.all()
        context = {'countries': countries_list}
        return render(request, 'country_admin.html', context)


class CountryCreateView(CreateView):
    template_name = 'country_create.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('administration')


class CountryUpdateView(UpdateView):
    template_name = 'country_create.html'
    model = Country
    form_class = CountryModelForm
    success_url = reverse_lazy('administration')


class CountryDeleteView(DeleteView):
    template_name = 'country_confirm_delete.html'
    model = Country
    success_url = reverse_lazy('administration')


# City


def city(request, pk):
    city_object = City.objects.get(id=pk)
    hotels = Hotel.objects.filter(city=city_object)
    context = {'city': city_object, 'hotels': hotels}
    return render(request, 'city.html', context)


class CityModelForm(ModelForm):
    class Meta:
        model = City
        fields = '__all__'

    def cleaned_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name'].strip().title()
        return name


class CityView(View):
    def get(self, request):
        cities_list = City.objects.all()
        context = {'cities': cities_list}
        return render(request, 'city_admin.html', context)


class CityCreateView(CreateView):
    template_name = 'city_create.html'
    form_class = CityModelForm
    success_url = reverse_lazy('administration')


class CityUpdateView(UpdateView):
    template_name = 'city_create.html'
    model = City
    form_class = CityModelForm
    success_url = reverse_lazy('administration')


class CityDeleteView(DeleteView):
    template_name = 'city_confirm_delete.html'
    model = City
    success_url = reverse_lazy('administration')


# Hotel


class HotelModelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'

    images = MultiFileField(min_num=1, max_num=8, max_file_size=1024*1024*5)

    def clean_name(self):
        initial_form = super().clean()
        initial = initial_form['name'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()

    def save(self, commit=True):
        instance = super().save(commit)
        images = self.cleaned_data.get('images')

        if images:
            for image in images:
                HotelImage.objects.create(hotel=instance, image=image)

        return instance


def hotel(request, pk):
    try:
        hotel_object = Hotel.objects.get(id=pk)
    except:
        return render(request, 'index.html')

    avg_rating = None
    if Rating.objects.filter(hotel=hotel_object).count() > 0:
        avg_rating = Rating.objects.filter(hotel=hotel_object).aggregate(Avg('rating'))

    user = request.user
    user_rating = None
    if request.user.is_authenticated:
        if Rating.objects.filter(hotel=hotel_object, user=user).count() > 0:
            user_rating = Rating.objects.get(hotel=hotel_object, user=user)

    comments = Comment.objects.filter(hotel=hotel_object).order_by('-created')

    images = HotelImage.objects.filter(hotel=hotel_object)

    travel_packages = TravelPackage.objects.filter(hotel=hotel_object)

    meal_plans = MealPlan.objects.all()

    current_travel_package = travel_packages.first()
    travel_package = TravelPackage
    arrival_date = travel_package.arrival_date
    departure_date = travel_package.departure_date

    context = {'hotel': hotel_object, 'avg_rating': avg_rating,
               'user_rating': user_rating, 'comments': comments, 'images': images, 'travel_packages': travel_packages,
               'meal_plans': meal_plans, 'arrival_date': arrival_date, 'departure_date': departure_date}
    return render(request, 'hotel.html', context)


class HotelView(View):
    def get(self, request):
        hotel_list = Hotel.objects.all()
        context = {'hotels': hotel_list}
        return render(request, 'hotel_admin.html', context)


class HotelsView(View):
    template_name = 'hotels.html'

    def get(self, request):
        form = HotelFilterForm(request.GET)

        queryset = Hotel.objects.all()

        if form.is_valid():
            continents = form.cleaned_data.get('continents')
            countries = form.cleaned_data.get('countries')
            cities = form.cleaned_data.get('cities')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            search_name = form.cleaned_data.get('search_name')
            star_rating = form.cleaned_data.get('star_rating', [])
            if isinstance(star_rating, list) and len(star_rating) == 1:
                star_rating = star_rating[0]

            if star_rating:
                queryset = queryset.filter(star_rating=star_rating)

            customer_rating_options = ['20', '40', '60', '70', '80', '90']
            selected_customer_ratings = [option for option in customer_rating_options if
                                         option in form.cleaned_data.get('customer_rating', [])]

            if selected_customer_ratings:
                queryset = queryset.filter(customer_rating__gte=min(map(int, selected_customer_ratings)))

            if continents:
                queryset = queryset.filter(city__country__continent__in=continents)
            if countries:
                queryset = queryset.filter(city__country__in=countries)
            if cities:
                queryset = queryset.filter(city__in=cities)
            if star_rating:
                queryset = queryset.filter(star_rating=star_rating)
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            if search_name:
                queryset = queryset.filter(name__icontains=search_name)

        # Řazení podle ceny
        sort_by_price = request.GET.get('sort_by_price', None)
        if sort_by_price == 'asc':
            queryset = queryset.order_by('price')
        elif sort_by_price == 'desc':
            queryset = queryset.order_by('-price')

        hotels = queryset

        context = {
            'hotels': hotels,
            'form': form,
        }
        return render(request, self.template_name, context)


class HotelCreateView(CreateView):
    template_name = 'hotel_create.html'
    form_class = HotelModelForm
    success_url = reverse_lazy('administration')


class HotelUpdateView(UpdateView):
    template_name = 'hotel_create.html'
    model = Hotel
    form_class = HotelModelForm
    success_url = reverse_lazy('administration')


class HotelDeleteView(DeleteView):
    template_name = 'hotel_confirm_delete.html'
    model = Hotel
    success_url = reverse_lazy('administration')


class HotelFilterForm(Form):
    continent = ModelMultipleChoiceField(queryset=Continent.objects.all(), required=False, label='Podle kontinentu')
    countries = ModelMultipleChoiceField(queryset=Country.objects.all(), required=False, label='Podle země')
    cities = ModelMultipleChoiceField(queryset=City.objects.all(), required=False, label='Podle města')
    STAR_RATINGS = [
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐'),
    ]

    star_rating = MultipleChoiceField(
        choices=STAR_RATINGS,
        widget=CheckboxSelectMultiple,
        required=False,
        label='Podle počtu hvězdiček',
    )

    min_price = DecimalField(validators=[MinValueValidator(0)])
    max_price = DecimalField(validators=[MinValueValidator(0)])
    search_name = CharField(max_length=100, required=False, label='Vyhledat podle názvu')

# Airport


def airport(request, pk):
    airport_object = Airport.objects.get(id=pk)
    airports = Airport.objects.filter(airport=airport_object)
    context = {'airport': airport_object, 'airports': airports}
    return render(request, 'airport.html', context)


class AirportForm(ModelForm):
    class Meta:
        model = Airport
        fields = '__all__'


class AirportView(View):
    def get(self, request):
        airport_list = Airport.objects.all()
        context = {'airports': airport_list}
        return render(request, 'airport_admin.html', context)


class AirportCreate(CreateView):
    template_name = 'airport_create.html'
    model = Airport
    form_class = AirportForm
    success_url = reverse_lazy('administration')


class AirportUpdate(UpdateView):
    template_name = 'airport_create.html'
    model = Airport
    form_class = AirportForm
    success_url = reverse_lazy('administration')


class AirportDelete(DeleteView):
    template_name = 'Airport_confirm_delete.html'
    model = Airport
    success_url = reverse_lazy('administration')


# Meal plan


def meal(request, pk):
    meal_object = MealPlan.objects.get(id=pk)
    meals = MealPlan.objects.filter(meal=meal_object)
    context = {'meal': meal_object, 'meals': meals}
    return render(request, 'meal.html', context)


class MealPlanForm(ModelForm):
    class Meta:
        model = MealPlan
        fields = '__all__'


class MealPlanView(View):
    def get(self, request):
        meal_list = MealPlan.objects.all()
        context = {'meals': meal_list}
        return render(request, 'meal_admin.html', context)


class MealCreate(CreateView):
    template_name = 'meal_create.html'
    model = MealPlan
    form_class = MealPlanForm
    success_url = reverse_lazy('administration')


class MealUpdate(UpdateView):
    template_name = 'meal_create.html'
    model = MealPlan
    form_class = MealPlanForm
    success_url = reverse_lazy('administration')


class MealDeleteView(DeleteView):
    template_name = 'meal_confirm_delete.html'
    model = MealPlan
    success_url = reverse_lazy('administration')


# Travel packages


class TravelPackageForm(ModelForm):
    class Meta:
        model = TravelPackage
        fields = '__all__'
        widgets = {
            'arrival_date': SelectDateWidget(years=range(datetime.now().year, datetime.now().year + 2)),
            'departure_date': SelectDateWidget(years=range(datetime.now().year, datetime.now().year + 2))
        }

    def clean(self):
        cleaned_data = super().clean()
        arrival_date = cleaned_data.get('arrival_date')
        departure_date = cleaned_data.get('departure_date')

        if arrival_date and arrival_date < datetime.today().date():
            self.add_error('arrival_date', 'Nelze vybrat datum příjezdu v minulosti.')

        if departure_date and departure_date < datetime.today().date():
            self.add_error('departure_date', 'Nelze vybrat datum odjezdu v minulosti.')

        if arrival_date and departure_date and arrival_date >= departure_date:
            self.add_error('departure_date', 'Datum odjezdu musí být po datu příjezdu.')

        return cleaned_data


def travel_package(request, pk):
    travel_package_object = TravelPackage.objects.get(id=pk)
    travel_packages = MealPlan.objects.filter(travel_package=travel_package_object)
    context = {'travel_package': travel_package_object, 'travel_packages': travel_packages}
    return render(request, 'travel_package.html', context)


class TravelPackageView(View):
    def get(self, request):
        travel_package_list = TravelPackage.objects.all()
        context = {'travel_packages': travel_package_list}
        return render(request, 'travel_package_admin.html', context)


class TravelPackageCreate(CreateView):
    template_name = 'travel_package_create.html'
    model = TravelPackage
    form_class = TravelPackageForm
    success_url = reverse_lazy('administration')

    def post(self, request, *args, **kwargs):
        print("POST method called")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        arrival_date = form.cleaned_data.get('arrival_date')
        departure_date = form.cleaned_data.get('departure_date')
        print(f"Arrival Date: {arrival_date}, Departure Date: {departure_date}")


class TravelPackageUpdate(UpdateView):
    template_name = 'travel_package_create.html'
    model = TravelPackage
    form_class = TravelPackageForm
    success_url = reverse_lazy('administration')


class TravelPackageDelete(DeleteView):
    template_name = 'travel_package_delete.html'
    model = TravelPackage
    success_url = reverse_lazy('administration')


# Transportation


class TransportationForm(ModelForm):
    class Meta:
        model = Transportation
        fields = '__all__'


def transportation(request, pk):
    transportation_object = Transportation.objects.get(id=pk)
    transportations = Transportation.objects.filter(transportation_object=transportation_object)
    context = {'transportation': transportation_object, 'transportations': transportations}
    return render(request, 'transportation.html', context)


class TransportationView(View):
    def get(self, request):
        transportation_list = Transportation.objects.all()
        context = {'transportations': transportation_list}
        return render(request, 'transportation_admin.html', context)


class TransportationCreate(CreateView):
    template_name = 'transportation_create.html'
    model = Transportation
    form_class = TransportationForm
    success_url = reverse_lazy('administration')


class TransportationUpdate(UpdateView):
    template_name = 'transportation_crete.html'
    model = Transportation
    form_class = TransportationForm
    success_url = reverse_lazy('administration')


class TransportationDelete(DeleteView):
    template_name = 'transportation_delete.html'
    model = Transportation
    success_url = reverse_lazy('administration')


# PURCHASE


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'


def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)

        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.customer = request.user
            purchase.save()

            return render(request, 'purchase_success.html', {'purchase': purchase})
    else:
        form = PurchaseForm()

    return render(request, 'purchase_form.html', {'form': form})
