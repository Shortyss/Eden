from datetime import datetime

import phonenumbers
from django.db.models import Model, OneToOneField, CASCADE, DateField, TextField, EmailField, CharField, IntegerField, \
    SET_NULL, ForeignKey, DO_NOTHING, ImageField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.forms import SelectDateWidget, DateInput
from rest_framework.exceptions import ValidationError


# Create your models here.


class PhoneNumberField(CharField):
    def to_python(self, value):
        try:
            phone_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError("Invalid phone number.")
            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException as e:
            raise ValidationError(f"Invalid phone number format: {e}")


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = CharField(max_length=25, null=True, blank=True, verbose_name='Telefon')
    birth_date = DateField(null=True, blank=True, verbose_name='Datum narození')
    street = CharField(max_length=255, null=True, blank=True, verbose_name='Ulice')
    house_number = IntegerField(null=True, blank=True, verbose_name='Číslo domu')
    city = CharField(max_length=132, null=True, blank=True, verbose_name='Město')
    country = CharField(max_length=132, null=True, blank=True, verbose_name='Země')
    postal_code = CharField(max_length=20, null=True, blank=True, verbose_name='PSČ')


class UserImage(Model):
    user = ForeignKey(Profile, on_delete=DO_NOTHING)
    image = ImageField(upload_to='users_image/')


