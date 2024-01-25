from datetime import date, datetime

from django.test import TestCase

from viewer.models import *


class LocationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        continent = Continent.objects.create(
            name='TestContinent'
        ),
        country = Country.objects.create(
            name='TestCountry',
        )
        city = City.objects.create(
            name='TestCity',
            country=country
        )

    def test_continent(self):
        continent = Continent.objects.get(id=1)
        self.assertEqual(continent.name, 'TestContinent')
        self.assertEqual(continent.__str__(), 'TestContinent')

    def test_country(self):
        country = Country.objects.get(id=1)
        self.assertEqual(country.name, 'TestCountry')
        self.assertEqual(country.__str__(), 'TestCountry')

    def test_City(self):
        city = City.objects.get(id=1)
        related_country = city.country
        self.assertEqual(city.name, 'TestCity')
        self.assertEqual(related_country.name, 'TestCountry')
        self.assertEqual(city.__str__(), 'TestCity - TestCountry')


class HotelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(name='TestCountry')
        city = City.objects.create(name='TestCity', country=country)
        airport = Airport.objects.create(name='TestAirport', airport_city=city)
        transportation = Transportation.objects.create(
            departure_airport=airport,
            arrival_airport=airport,
            price=1000.00
        )
        hotel = Hotel.objects.create(
            name='TestHotel',
            single_rooms=2,
            double_rooms=2,
            family_rooms=2,
            suite_rooms=2,
            travelers=1,
            current_price=1000.00,
            total_price=2000.00,
            star_rating=5,
            description='Hotel description',
            city=city,
            transportation=transportation,
            country=country,
        )
        hotel.save()

    def test_hotel_name(self):
        hotel = Hotel.objects.get(id=1)
        self.assertEqual(hotel.name, 'TestHotel')

    def test_hotel_rooms(self):
        hotel = Hotel.objects.get(id=1)
        self.assertEqual(hotel.single_rooms, 2)
        self.assertEqual(hotel.double_rooms, 2)
        self.assertEqual(hotel.family_rooms, 2)
        self.assertEqual(hotel.suite_rooms, 2)

    def test_travelers(self):
        hotel = Hotel.objects.get(id=1)
        self.assertEqual(hotel.travelers, 1)

    def test_current_price(self):
        hotel = Hotel.objects.get(id=1)
        self.assertEqual(hotel.current_price, 1000.00)

    def test_total_price(self):
        hotel = Hotel.objects.get(id=1)
        self.assertEqual(hotel.total_price, 2000.00)

    def test_star_rating(self):
        hotel = Hotel.objects.get(id=1)
        self.assertEqual(hotel.star_rating, 5)

    def test_description(self):
        hotel = Hotel.objects.get(id=1)
        self.assertEqual(hotel.description, 'Hotel description')

    def test_city(self):
        hotel = Hotel.objects.get(id=1)
        expected_city_str = 'TestCity - TestCountry'
        self.assertEqual(str(hotel.city), expected_city_str)

    def test_transportation_str(self):
        hotel = Hotel.objects.get(id=1)
        transportation = hotel.transportation
        string = f"{transportation.departure_airport.name} ({transportation.departure_airport.airport_city.name}) - " \
                 f"{transportation.arrival_airport.name} ({transportation.arrival_airport.airport_city.name}) : " \
                 f"{transportation.price}"
        assert string == "TestAirport (TestCity) - TestAirport (TestCity) : 1000.00"

    def test_hotel_country(self):
        hotel = Hotel.objects.get(id=1)
        expected_country_str = 'TestCountry'
        self.assertEqual(str(hotel.country), expected_country_str)


class MealPlanTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        meal_plan = MealPlan.objects.create(name='TestMeal', price=100.00)

    def test_meal_plan(self):
        meal_plan = MealPlan.objects.get(id=1)
        self.assertEqual(meal_plan.name, 'TestMeal')
        self.assertEqual(meal_plan.price, 100.00)
        self.assertEqual(meal_plan.__str__(), 'TestMeal, 100.00')


class TravelerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        traveler = Traveler.objects.create(
            first_name='TestTraveler',
            last_name='Doe',
            birth_date=date(2000, 12, 12)
        )

    def test_traveler_name(self):
        traveler = Traveler.objects.get(id=1)
        self.assertEqual(traveler.first_name, 'TestTraveler')
        self.assertEqual(traveler.last_name, 'Doe')

    def test_traveler_birth_date(self):
        traveler = Traveler.objects.get(id=1)
        expected_birth_date = date(2000, 12, 12)
        self.assertEqual(traveler.birth_date, expected_birth_date)

    def test_traveler_string(self):
        traveler = Traveler.objects.get(id=1)
        self.assertEqual(traveler.__str__(), 'TestTraveler Doe')


class PurchaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        continent = Continent.objects.create(name='Continent')

        country = Country.objects.create(name='Country',
                                         continent=continent)

        city = City.objects.create(name='City',
                                   country=country)

        airport = Airport.objects.create(name='Airport',
                                         airport_city=city)

        transportation = Transportation.objects.create(departure_airport=airport,
                                                        arrival_airport=airport,
                                                        price=2000)

        hotel = Hotel.objects.create(name='HotelTest', city=city,
                                     transportation=transportation,
                                     single_room=1,
                                     travelers=1,
                                     current_price=5000,
                                     total_price=5000)

        meal_plan = MealPlan.objects.create(name='Polopenze',
                                            price=1000)

        traveler = Traveler.objects.create(first_name='Jan',
                                           last_name='Novák',
                                           birth_date='1980-10-04')

        purchase = Purchase.objects.create(customer=traveler,
                                            hotel=hotel,
                                            meal_plan=meal_plan,
                                            arrival_date='2024-10-04',
                                            departure_date='2024-10-11')

    def TestPurchase(self):
        purchase = Purchase.objects.get(id=1)
        self.assertEqual(purchase.hotel, 'HotelTest')

    def TestTraveler(self):
        purchase = Purchase.objects.get(id=1)
        self.assertEqual(purchase.travelers, 1)

    def TestPrice(self):
        purchase = Purchase.objects.get(id=1)
        self.assertEqual(purchase.total_price, 6000)

    def TestArrivalDate(self):
        purchase = Purchase.objects.get(id=1)
        self.assertEqual(purchase.arrival_date, datetime.date(2024, 10, 4))

    def TestDepartureDate(self):
        purchase = Purchase.objects.get(id=1)
        self.assertEqual(purchase.departure_date, datetime.date(2024, 10, 11))

    def TestMealPlan(self):
        purchase = Purchase.objects.get(id=1)
        self.assertEqual(purchase.meal_plan, 'Polopenze')


class PricesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        continent = Continent.objects.create(name='Continent')

        country = Country.objects.create(name='Country',
                                         continent=continent)

        city = City.objects.create(name='City',
                                   country=country)

        airport = Airport.objects.create(name='Airport',
                                         airport_city=city)

        transportation = Transportation.objects.create(departure_airport=airport,
                                                        arrival_airport=airport,
                                                        price=2000)

        hotel = Hotel.objects.create(name='HotelTest', city=city,
                                     transportation=transportation,
                                     single_room=1,
                                     doubles_room=1,
                                     travelers=2,
                                     current_price=5000,
                                     total_price=5000)

        prices = Prices.objects.create(hotel=hotel,
                                      arrival_date='2024-10-04',
                                      departure_date='2024-10-11',
                                      price_single_room=1000,
                                      price_double_room=1500,
                                      price_family_room=2000,
                                      price_suite=3000)

    def TestPricesHotel(self):
        prices = Prices.objects.get(id=1)
        self.assertEqual(prices.hotel, 'HotelTest')

    def TestPricesDate(self):
        prices = Prices.objects.get(id=1)
        self.assertEqual(prices.arrival_date, datetime.date(2024, 10, 4))
        self.assertEqual(prices.departure_date, datetime.date(2024, 10, 11))

    def TestPrices(self):
        prices = Prices.objects.get(id=1)
        self.assertEqual(prices.price_single_room, 1000)
        self.assertEqual(prices.price_double_room, 1500)
        self.assertEqual(prices.price_family_room, 2000)
        self.assertEqual(prices.price_suite, 3000)


class RatingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
