from logging import getLogger

from django.core.files.base import ContentFile
from django.forms import ModelForm, Form, ModelMultipleChoiceField, ChoiceField, Select, Textarea, inlineformset_factory
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from viewer.models import *

# Create your views here.
LOGGER = getLogger()


def index(request):
    return render(request, 'index.html')


# Image form

class ImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['image', 'description']


# CONTINENT


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
        return render(request, 'continents.html', context)


class ContinentCreateView(CreateView):
    template_name = 'continent_create.html'
    form_class = ContinentModelForm
    success_url = reverse_lazy('administration')


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
    template_name = 'country_admin.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('administration')


class CountryUpdateView(UpdateView):
    template_name = 'country_admin.html'
    model = Country
    form_class = CountryModelForm
    success_url = reverse_lazy('administration')


class CountryDeleteView(DeleteView):
    template_name = 'country_confirm_delete.html'
    model = Country
    success_url = reverse_lazy('administration')


# City


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
    template_name = 'city_admin.html'
    form_class = CityModelForm
    success_url = reverse_lazy('administration')


class CityUpdateView(UpdateView):
    template_name = 'city_admin.html'
    model = City
    form_class = CityModelForm
    success_url = reverse_lazy('administration')


class CityDeleteView(DeleteView):
    template_name = 'city_confirm_delete.html'
    model = City
    success_url = reverse_lazy('administration')


# Hotel


class HotelForm(Form):
    name = CharField(max_length=132)
    city = ModelMultipleChoiceField(queryset=City.objects)
    star_rating = ChoiceField(choices=[
        (1, '1 hvězdička'),
        (2, '2 hvězdičky'),
        (3, '3 hvězdičky'),
        (4, '4 hvězdičky'),
        (5, '5 hvězdiček')],
        widget=Select(attrs={'class': 'form-control'})
    )
    description = CharField(widget=Textarea, required=False)

    def clean_name(self):
        initial_form = super().clean()
        initial = initial_form['name'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()


class HotelCreateView(CreateView):
    template_name = 'hotel_create.html'
    form_class = HotelForm
    success_url = reverse_lazy('administration')

    def form_valid(self, form):
        result = super().form_valid(form)

        ImagesFormSet = inlineformset_factory(Hotel, Images, form=ImageForm, extra=4)

        formset = ImagesFormSet(self.request.POST, self.request.FILES, instance=self.object)

        if formset.is_valid():
            formset.save()

        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_valid(form)


class HotelUpdateView(UpdateView):
    template_name = 'hotel_create.html'
    model = Hotel
    success_url = reverse_lazy('administration')


class HotelDeleteView(DeleteView):
    template_name = 'hotel_confirm_delete.html'
    model = Hotel
    success_url = reverse_lazy('administration')

# def Hotels(request):
#     c = request.GET.get('continent', '')
#     co = request.GET.get('country', '')
#     ci = request.GET.get('city', '')
#     continents = Continent.objects.all()
#     if c != '' and co != '' and ci != '':
#         c = int(c)
#         co = int(co)
#         ci = int(ci)
#         if (Continent.objects.filter(id=c).exists()
#                 and Country.objects.filter(id=co).exists() and City.objects.filter(id=ci).exists()):
#             continent = Continent.objects.get(id=c)
#             country = Country.objects.get(id=co)
#             city = City.objects.get(id=ci)
#             hotel_list = Hotel.objects.filter(cities=city, countries=country, continents=continent)
#             context = {'hotels': hotel_list, 'continents': continents, 'filtered_by': f'podle kontinentu {continent} a země {country}.'}
#             return render(request, 'hotels.html', context)


