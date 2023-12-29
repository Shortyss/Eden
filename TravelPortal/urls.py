"""
URL configuration for TravelPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import rest_framework
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from TravelPortal import settings
from accounts.views import *
from viewer.models import *
from viewer.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),

    path('accounts/login/', LoginView.as_view(), name='login'),  # vlastní view
    path('accounts/signup/', SignUpView.as_view(), name='signup'),  # vlastní view
    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/profile_create/<pk>', ProfileCreateView.as_view(), name='profile_create'),
    path('accounts/profile/<pk>/', profile, name='profile'),
    path('accounts/profile_edit/', profile_edit, name='profile_edit'),

    path('administration/', administration, name='administration'),

    path('continent_admin/', ContinentView.as_view(), name='continent_admin'),
    path('continent/<pk>/', continent, name='continent'),
    path('continent_create/', ContinentCreateView.as_view(), name='continent_create'),
    path('continents/update/<pk>/', ContinentUpdateView.as_view(), name='continent_update'),
    path('continents/delete/<pk>/', ContinentDeleteView.as_view(), name='continent_delete'),

    path('country_admin', CountryView.as_view(), name='country_admin'),
    path('country/<pk>/', country, name='country'),
    path('country_create/', CountryCreateView.as_view(), name='country_create'),
    path('countries/update/<pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('countries/delete/<pk>/', CountryDeleteView.as_view(), name='country_delete'),

    path('city_admin/', CityView.as_view(), name='city_admin'),
    path('city/<pk>/', city, name='city'),
    path('city_create/', CityCreateView.as_view(), name='city_create'),
    path('cities/update/<pk>/', CityUpdateView.as_view(), name='city_update'),
    path('cities/delete/<pk>/', CityDeleteView.as_view(), name='city_delete'),

    path('hotel_admin/', HotelView.as_view(), name='hotel_admin'),
    path('hotel/<pk>/', hotel, name='hotel'),
    path('hotel_create/', HotelCreateView.as_view(), name='hotel_create'),
    path('hotels/update/<pk>', HotelUpdateView.as_view(), name='hotel_update'),
    path('hotels/delete/<pk>/', HotelDeleteView.as_view(), name='hotel_delete'),

    path('europe/<pk>/', EuropeCountriesView.as_view(), name='europe'),
    path('america/<pk>/', AmericaCountriesView.as_view(), name='america'),
    path('asia/<pk>/', AsiaCountriesView.as_view(), name='asia'),
    path('africa/<pk>/', AfricaCountriesView.as_view(), name='africa'),

    path('rate_hotel/', rate_hotel, name='rate_hotel'),
    path('add_comment/', add_comment, name='add_comment'),

    path('meal_admin/', MealPlanView.as_view(), name='meal_admin'),
    path('meal/<pk>/', meal, name='meal'),
    path('meal_create/', MealCreate.as_view(), name='meal_create'),
    path('meals/update/<pk>/', MealUpdate.as_view(), name='meal_update'),
    path('meals/delete/<pk>', MealDeleteView.as_view(), name='meal_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
