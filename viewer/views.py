from logging import getLogger
from viewer.models import *
from django.core.files.base import ContentFile
from django.db.models import Avg
from django.forms import ModelForm, Form, ModelMultipleChoiceField, ChoiceField, Select, inlineformset_factory, \
    CharField, Textarea, ClearableFileInput, FileField, HiddenInput
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

    def get(self, request, *args, **kwargs):
        continent_id = kwargs.get('pk')
        countries = Country.objects.filter(continent__id=continent_id)
        return render(request, self.template_name, {'countries': countries})


class EuropeCountriesView(ContinentCountriesView):
    template_name = 'europe.html'


class AmericaCountriesView(ContinentCountriesView):
    template_name = 'america.html'


class AsiaCountriesView(ContinentCountriesView):
    template_name = 'asia.html'


class AfricaCountriesView(ContinentCountriesView):
    template_name = 'africa.html'


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
        name = cleaned_data['name'].strip().capitalize()
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
        name = cleaned_data['name'].strip().capitalize()
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

    def clean_name(self):
        initial_form = super().clean()
        initial = initial_form['name'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()


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

    images = Image.objects.filter(hotel=hotel_object)

    context = {'hotel': hotel_object, 'avg_rating': avg_rating,
               'user_rating': user_rating, 'comments': comments, 'images': images}
    return render(request, 'hotel.html', context)


class HotelView(View):
    def get(self, request):
        hotel_list = Hotel.objects.all()
        context = {'hotels': hotel_list}
        return render(request, 'hotel_admin.html', context)


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

