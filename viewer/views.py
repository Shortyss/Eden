import json
from logging import getLogger

from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.validators import MinValueValidator
from django.forms.widgets import ChoiceWidget
from django.http import HttpResponse, HttpResponseRedirect
from django_addanother.views import CreatePopupMixin
from django_addanother.widgets import AddAnotherWidgetWrapper

from viewer.models import *
from django.db.models import Avg, Q, F
from django.forms import ModelForm, Form, ModelMultipleChoiceField, ChoiceField, Select, inlineformset_factory, \
    CharField, Textarea, ClearableFileInput, FileField, HiddenInput, FileInput, SelectDateWidget, forms, \
    CheckboxSelectMultiple, MultipleChoiceField, SelectMultiple, DateInput, TextInput, ModelChoiceField
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from datetime import datetime

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


class ContinentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'continent_create.html'
    form_class = ContinentModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


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


class ContinentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'continent_create.html'
    model = Continent
    form_class = ContinentModelForm
    success_url = reverse_lazy('administration')


class ContinentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'continent_confirm_delete.html'
    model = Continent
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


# COUNTRY


def country(request, pk):
    country_object = Country.objects.get(id=pk)
    cities = City.objects.filter(country=country_object)
    context = {'country': country_object, 'cities': cities}
    return render(request, 'country.html', context)


class CountryModelForm(ModelForm,CreatePopupMixin):

    class Meta:
        model = Country
        fields = '__all__'

        widgets = {
            'continent': AddAnotherWidgetWrapper(
               Select,
                reverse_lazy('continent_create')
            )}

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name'].strip().title()
        return name


class CountryView(View):
    def get(self, request):
        countries_list = Country.objects.all().order_by('name')
        context = {'countries': countries_list}
        return render(request, 'country_admin.html', context)


class CountryCreateView(CreatePopupMixin, CreateView):
    template_name = 'country_create.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


class CountryUpdateView(UpdateView):
    template_name = 'country_create.html'
    model = Country
    form_class = CountryModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


class CountryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'country_confirm_delete.html'
    model = Country
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


# Island


def island(request, pk):
    island_object = Island.objects.get(id=pk)
    cities = City.objects.filter(island=island_object)
    context = {'island': island_object, 'cities': cities}
    return render(request, 'island.html', context)


class IslandModelForm(ModelForm,CreatePopupMixin):
    class Meta:
        model = Island
        fields = '__all__'

        widgets = {
            'country': AddAnotherWidgetWrapper(
                autocomplete.ModelSelect2(
                    url='country_autocomplete',
                    forward=['country'],
                ),
                reverse_lazy('country_create')
            ),
            'city': AddAnotherWidgetWrapper(
                autocomplete.ModelSelect2(
                    url='city_autocomplete',
                    forward=['city'],
                ),
                reverse_lazy('city_create')
            )
        }

        def cleaned_name(self):
            cleaned_data = super().clean()
            name = cleaned_data['name'].strip().title()
            return name


class IslandView(View):
    def get(self, request):
        user_role = 'administration'

        if user_role == 'administration':
            island_list = Island.objects.all().order_by('name')
            context = {'islands': island_list}
            return render(request, 'island_admin.html', context)
        else:
            return render(request, 'islands.html')


class IslandCreateView(LoginRequiredMixin, CreatePopupMixin, CreateView):
    template_name = 'island_create.html'
    form_class = IslandModelForm
    success_url = reverse_lazy('administration')
    permission_request = 'administration'


class IslandUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'island_create.html'
    form_class = IslandModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


class IslandDelete(LoginRequiredMixin, DeleteView):
    template_name = 'Island_delete.html'
    model = Island
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


# City


def city(request, pk):
    city_object = City.objects.get(id=pk)
    hotels = Hotel.objects.filter(city=city_object)
    context = {'city': city_object, 'hotels': hotels}
    return render(request, 'city.html', context)


class CityModelForm(ModelForm,CreatePopupMixin):
    class Meta:
        model = City
        fields = '__all__'

        widgets = {
            'country': AddAnotherWidgetWrapper(
                autocomplete.ModelSelect2(
                    url='country_autocomplete',
                    forward=['country'],
                ),
                reverse_lazy('country_create')
            )}

    def cleaned_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name'].strip().title()
        return name


class CityView(View):
    def get(self, request):
        cities_list = City.objects.all().order_by('name')
        context = {'cities': cities_list}
        return render(request, 'city_admin.html', context)


class CityCreateView(LoginRequiredMixin, CreatePopupMixin, CreateView):
    template_name = 'city_create.html'
    form_class = CityModelForm
    success_url = reverse_lazy('administration')
    permission_request = 'administration'


class CityUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'city_create.html'
    model = City
    form_class = CityModelForm
    success_url = reverse_lazy('administration')
    permission_request = 'administration'


class CityDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'city_confirm_delete.html'
    model = City
    success_url = reverse_lazy('administration')
    permission_request = 'administration'


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
# Price


class PricesForm(ModelForm):
    class Meta:
        model = Prices
        fields = '__all__'
        widgets = {
            'arrival_date': DateInput(attrs={'type': 'date'}),
            'departure_date': DateInput(attrs={'type': 'date'})
        }


def add_price(request):
    if request.method == 'POST':
        form = PricesForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('administration')
    else:
        form = PricesForm()

    return render(request, 'add_price.html', {'form': form})


HotelPricesFormSet = inlineformset_factory(Hotel, Prices, form=PricesForm, extra=7, can_delete=True)

# Hotel


class HotelModelForm(ModelForm, CreatePopupMixin):
    class Meta:
        model = Hotel
        fields = '__all__'
        exclude = ['country', 'Island']

        widgets = {
            'city': AddAnotherWidgetWrapper(
                autocomplete.ModelSelect2(
                    url='city_autocomplete'
                ),
                reverse_lazy('city_create')
            ),
            'country': autocomplete.ModelSelect2(
                url='country_autocomplete'
            ),
            'transportation': AddAnotherWidgetWrapper(
                Select,
                reverse_lazy('transportation_create')
            ),
        }
    prices = HotelPricesFormSet()

    country = CharField(widget=HiddenInput(), required=False)

    images = MultiFileField(required=False, min_num=1, max_num=15, max_file_size=1024*1024*5)

    def clean_name(self):
        initial_form = super().clean()
        initial = initial_form['name'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()

    def save(self, commit=True):
        instance = super().save(commit=False)
        images = self.cleaned_data.get('images')

        if commit:
            instance.save()

        if images:
            for image in images:
                HotelImage.objects.create(hotel=instance, image=image)

        return instance


def hotel(request, pk):
    try:
        hotel_object = Hotel.objects.get(id=pk)
        request.session['hotel_name'] = hotel_object.name
        request.session['hotel_id'] = hotel_object.id
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

    meal_plans = MealPlan.objects.all()

    current_date = datetime.now()
    week_later_date = current_date + timedelta(days=7)

    double_room_prices = Prices.objects.filter(
        hotel=hotel_object,
        price_double_room__isnull=False,
        arrival_date__lte=current_date,
        departure_date__gte=week_later_date
    ).order_by('-arrival_date').first()

    if double_room_prices:
        nights_in_week = (week_later_date - current_date).days
        total_price_for_week = double_room_prices.price_double_room * nights_in_week

        hotel_object.current_price = total_price_for_week
        hotel_object.save()

    prices = list(Prices.objects.filter(hotel=hotel_object).values())
    for price in prices:
        date_columns = ['arrival_date', 'departure_date']
        for column in date_columns:
            if column in price and price[column] is not None:
                price[column] = price[column].strftime('%Y-%m-%d')

        for key, value in price.items():
            if isinstance(value, Decimal):
                price[key] = float(value)

    if request.method == 'POST':
        single_rooms = int(request.POST.get('single_rooms', 0))
        double_rooms = int(request.POST.get('double_rooms', 0))
        family_rooms = int(request.POST.get('family_rooms', 0))
        suite_rooms = int(request.POST.get('suite_rooms', 0))

        transportation = request.POST.get('transportation')
        travelers = int(request.POST.get('travelers'))
        total_price = request.POST.get('total_price', '').strip()

        request.session['room_counts'] = {
            'single_rooms': single_rooms,
            'double_rooms': double_rooms,
            'family_rooms': family_rooms,
            'suite_rooms': suite_rooms,
            'transportation': transportation,
            'travelers': travelers,
            'total_price': total_price,
        }
        return redirect('purchase_create')

    context = {'hotel': hotel_object, 'avg_rating': avg_rating,
               'user_rating': user_rating, 'comments': comments, 'images': images,
               'meal_plans': meal_plans,
               'double_room_prices': double_room_prices,
               'prices': json.dumps(prices),
               }
    return render(request, 'hotel.html', context)


class HotelView(View):
    def get(self, request):
        hotel_list = Hotel.objects.all()
        context = {'hotels': hotel_list}
        return render(request, 'hotel_admin.html', context)


class HotelsView(View):
    def get(self, request):
        form = HotelFilterForm(request.GET)

        queryset = Hotel.objects.all()

        if form.is_valid():
            continents = form.cleaned_data.get('continent')
            countries = form.cleaned_data.get('countries')
            cities = form.cleaned_data.get('cities')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            search_name = form.cleaned_data.get('search_name')

            selected_star_ratings = form.cleaned_data.get('star_rating', [])
            if selected_star_ratings:
                queryset = queryset.filter(star_rating__in=selected_star_ratings)

            selected_customer_ratings = form.cleaned_data.get('customer_rating', [])
            if selected_customer_ratings:

                customer_rating_values = [int(rating) for rating in selected_customer_ratings]

                queryset = queryset.filter(rating__rating__gte=max(customer_rating_values))

            if continents:
                queryset = queryset.filter(city__country__continent__in=continents)
            if countries:
                queryset = queryset.filter(city__country__in=countries)
            if cities:
                queryset = queryset.filter(city__in=cities)
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            if search_name and len(search_name) >= 3:
                queryset = queryset.filter(name__icontains=search_name)

        # Řazení podle ceny
        sort_by_price = request.GET.get('sort_by_price', None)
        if sort_by_price == 'asc':
            queryset = queryset.order_by('current_price')
        elif sort_by_price == 'desc':
            queryset = queryset.order_by('-current_price')

        hotels = queryset

        context = {
            'hotels': hotels,
            'form': form,
        }
        return render(request, 'hotels.html', context)


class HotelCreateView(LoginRequiredMixin, CreateView):
    template_name = 'hotel_create.html'
    form_class = HotelModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'

    def form_valid(self, form):
        self.object = form.save(commit=True)
        city = form.cleaned_data.get('city')
        country = city.country if city else None
        self.object.country = country
        self.object.save()

        prices_formset = HotelPricesFormSet(self.request.POST, instance=self.object)

        if prices_formset.is_valid():
            prices_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form, prices_formset):
        prices_formset = form.prices
        return self.render_to_response(self.get_context_data(form=form, prices_formset=prices_formset))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['city'] = None
        data['country'] = None
        data['prices_formset'] = HotelPricesFormSet(instance=self.object)
        return data


class HotelUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'hotel_create.html'
    model = Hotel
    form_class = HotelModelForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        city = form.cleaned_data.get('city')
        country = city.country if city else None
        self.object.country = country
        self.object.save()

        prices_formset = HotelPricesFormSet(self.request.POST, instance=self.object)
        # add_price(self.request)
        if prices_formset.is_valid():
            prices_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        prices_formset = HotelPricesFormSet(self.request.POST, instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, prices_formset=prices_formset))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['city'] = None
        data['country'] = None
        data['prices_formset'] = HotelPricesFormSet(instance=self.object)
        return data


class HotelDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'hotel_confirm_delete.html'
    model = Hotel
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


def country_autocomplete(request):
    countries = Country.objects.all()
    json_data = {"countries": countries}
    return HttpResponse(json.dumps(json_data), content_type="application/javascript")


class HotelFilterForm(Form, CreatePopupMixin):
    continent = ModelMultipleChoiceField(queryset=Continent.objects.all(), required=False, label='Podle kontinentu',
                                         widget=CheckboxSelectMultiple)

    country = ModelMultipleChoiceField(
        queryset=Country.objects.all().order_by('name'),
        required=False,
        label='Podle země',
        widget=autocomplete.ModelSelect2Multiple(
            url='country_autocomplete',
            attrs={'data-placeholder': 'Začněte psát název země...'}
        )
    )

    cities = ModelMultipleChoiceField(
        queryset=City.objects.all().order_by('name'),
        required=False,
        label='Podle města',
        widget=autocomplete.ModelSelect2Multiple(
            url='city_autocomplete',
            attrs={'data-placeholder': 'Začněte psát název města...'}
        )
    )
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

    CUSTOMER_RATING_CHOICES = [
        ('60', '60 a více'),
        ('70', '70 a více'),
        ('80', '80 a více'),
        ('90', '90 a více'),
    ]

    customer_rating = MultipleChoiceField(
        choices=CUSTOMER_RATING_CHOICES,
        widget=CheckboxSelectMultiple,
        required=False,
        label='Hodnocení zákaznůků '
    )

    min_price = DecimalField(validators=[MinValueValidator(0)])
    max_price = DecimalField(validators=[MinValueValidator(0)])


# Airport


def airport(request, pk):
    airport_object = Airport.objects.get(id=pk)
    airports = Airport.objects.filter(airport=airport_object)
    context = {'airport': airport_object, 'airports': airports}
    return render(request, 'airport.html', context)


class AirportForm(ModelForm,CreatePopupMixin):
    class Meta:
        model = Airport
        fields = '__all__'

        widgets = {
            'airport_city': AddAnotherWidgetWrapper(
                Select,
                reverse_lazy('city_create')
            )}


class AirportView(View):
    def get(self, request):
        airport_list = Airport.objects.all()
        context = {'airports': airport_list}
        return render(request, 'airport_admin.html', context)


class AirportCreate(LoginRequiredMixin, CreatePopupMixin, CreateView):
    template_name = 'airport_create.html'
    model = Airport
    form_class = AirportForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


class AirportUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'airport_create.html'
    model = Airport
    form_class = AirportForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


class AirportDelete(LoginRequiredMixin, DeleteView):
    template_name = 'Airport_confirm_delete.html'
    model = Airport
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


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


class MealCreate(LoginRequiredMixin, CreateView):
    template_name = 'meal_create.html'
    model = MealPlan
    form_class = MealPlanForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


class MealUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'meal_create.html'
    model = MealPlan
    form_class = MealPlanForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


class MealDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'meal_confirm_delete.html'
    model = MealPlan
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


# Transportation


class TransportationForm(LoginRequiredMixin, CreatePopupMixin, ModelForm):
    class Meta:
        model = Transportation
        fields = '__all__'

        widgets = {
            'departure_airport': autocomplete.ModelSelect2(
                url='airport_autocomplete',
                forward=['arrival_airport'],
            ),
            'arrival_airport': autocomplete.ModelSelect2(
                url='airport_autocomplete',
                forward=['departure_airport'],
            ),
        }


def transportation(request, pk):
    try:
        transportation_object = Transportation.objects.get(id=pk)
        transportations = Transportation.objects.filter(id=pk)

        request.session['transportation_id'] = transportation_object.id

        context = {'transportation': transportation_object, 'transportations': transportations}
        return render(request, 'transportation.html', context)
    except Transportation.DoesNotExist:

        return HttpResponse("Doprava nebyla nalezena.", status=404)


class TransportationView(View):
    def get(self, request):
        transportation_list = Transportation.objects.all()
        context = {'transportations': transportation_list}
        return render(request, 'transportation_admin.html', context)


class TransportationCreate(LoginRequiredMixin, CreateView):
    template_name = 'transportation_create.html'
    model = Transportation
    form_class = TransportationForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


class TransportationUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'transportation_creete.html'
    model = Transportation
    form_class = TransportationForm
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


class TransportationDelete(LoginRequiredMixin, DeleteView):
    template_name = 'transportation_delete.html'
    model = Transportation
    success_url = reverse_lazy('administration')
    permission_required = 'administration'


# Traveler


class TravelerForm(ModelForm):
    class Meta:
        model = Traveler
        fields = '__all__'

        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
        }


# PURCHASE


class PurchaseForm(ModelForm):

    class Meta:
        model = Purchase
        fields = ['arrival_date', 'departure_date', 'meal_plan', 'single_rooms', 'double_rooms', 'family_rooms',
                  'suite_rooms', 'total_price', 'transportation', 'travelers', 'special_requirements']
        # readonly_fields = ['hotel_id', 'meal_plan']
        hotel = CharField(
            widget=TextInput(attrs={'readonly': 'readonly'})
        )
        widgets = {
            'hotel': TextInput(attrs={'readonly': 'readonly'}),
            'arrival_date': TextInput(attrs={'readonly': 'readonly'}),
            'departure_date': TextInput(attrs={'readonly': 'readonly'}),
            'meal_plan': TextInput(attrs={'readonly': 'readonly'}),
            'single_rooms': TextInput(attrs={'readonly': 'readonly'}),
            'double_rooms': TextInput(attrs={'readonly': 'readonly'}),
            'family_rooms': TextInput(attrs={'readonly': 'readonly'}),
            'suite_rooms': TextInput(attrs={'readonly': 'readonly'}),
            'transportation': TextInput(attrs={'readonly': 'readonly'}),
            'travelers': TextInput(attrs={'readonly': 'readonly'}),
            'total_price': TextInput(attrs={'readonly': 'readonly'})
        }


class PurchaseCreate(View):
    template_name = 'purchase_create.html'

    def post(self, request, *args, **kwargs):
        purchase_form = PurchaseForm(request.POST)
        travelers_forms = []
        travelers_list = []

        if purchase_form.is_valid():
            purchase = purchase_form.save(commit=False)
            purchase.customer = request.user
            hotel_id = request.POST.get('hotel_id')
            hotel_instance = Hotel.objects.get(pk=int(hotel_id))
            purchase.hotel = hotel_instance
            purchase.arrival_date = request.POST.get('arrival_date')
            purchase.departure_date = request.POST.get('departure_date')
            purchase.meal_plan_id = request.POST.get('meal_plan')
            purchase.number_of_single_rooms = request.POST.get('single_rooms')
            purchase.number_of_double_rooms = request.POST.get('double_rooms')
            purchase.number_of_family_rooms = request.POST.get('family_rooms')
            purchase.number_of_suites = request.POST.get('suite_rooms')
            purchase.transportation_id = request.POST.get('transportation')
            purchase.total_price = request.POST.get('total_price')

            num_travelers = int(request.POST.get('travelers', 0))
            for i in range(num_travelers):
                traveler_form = TravelerForm(request.POST, prefix=f'travelers_{i}')
                if traveler_form.is_valid():
                    traveler = traveler_form.save(commit=False)
                    travelers_forms.append(traveler_form)
                    if traveler.first_name and traveler.last_name:
                        traveler.purchase = purchase
                        traveler.save()

                        travelers_list.append(traveler)

                else:
                    travelers_forms.append(TravelerForm(prefix=f'number_of_travelers_{i}'))

            meal_plan_id = purchase.meal_plan_id
            meal_plan_instance = MealPlan.objects.get(pk=meal_plan_id)
            meal_plan_str = str(meal_plan_instance)

            transportation_id = purchase.transportation_id
            transportation_instance = Transportation.objects.get(pk=transportation_id)
            transportation_str = str(transportation_instance)

            travelers = int(request.POST.get('travelers', 0))
            if request.POST.get('step') == "1":
                return render(request, 'purchase_create.html', {'purchase_form': purchase_form,
                                                                'meal_plan': meal_plan_str,
                                                                'traveler_forms': travelers_forms,
                                                                'travelers': travelers})
            purchase.save()

            single_rooms = int(purchase.number_of_single_rooms)
            double_rooms = int(purchase.number_of_double_rooms)
            family_rooms = int(purchase.number_of_family_rooms)
            suite_rooms = int(purchase.number_of_suites)

            hotel_instance = purchase.hotel

            for traveler in travelers_list:
                purchase.traveler.add(traveler)
            purchase.save()
            return render(request, 'purchase_success.html', {'purchase_form': purchase_form,
                                                             'meal_plan': meal_plan_str,
                                                             'transportation': transportation_str,
                                                             'customer': purchase.customer,
                                                             'hotel_name': purchase.hotel,
                                                             'total_price': purchase.total_price,
                                                             'arrival_date': purchase.arrival_date,
                                                             'departure_date': purchase.departure_date,
                                                             'traveler_forms': travelers_forms, 'travelers': travelers})
        else:
            return render(request, 'purchase_create.html', {'purchase_form': purchase_form,
                                                            'traveler_forms': travelers_forms})


class PurchaseDetail(View):
    template_name = 'purchase_detail.html'

    def get(self, request, pk):
        purchase_object = Purchase.objects.get(pk=pk)
        context = {'purchase': purchase_object}
        return render(request, self.template_name, context)


def purchase_success(request, pk):
    purchase = Purchase.objects.get(pk=pk)
    context = {'purchase': purchase}
    return render(request, 'purchase_success.html', context)


