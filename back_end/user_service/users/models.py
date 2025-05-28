from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField

from .utils import constants


class CustomUser(AbstractUser):
    currency = models.CharField(max_length=3, default=constants.DEFAULT_CURRENCY)
    country = CountryField(default=constants.DEFAULT_REGION, blank=True)
    phone_number = PhoneNumberField(region=constants.DEFAULT_REGION, blank=True, null=True)
    monthly_income = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=constants.DEFAULT_CURRENCY,
        blank=True,
        null=True
    )
    financial_goal = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=constants.DEFAULT_CURRENCY,
        blank=True,
        null=True
    )
    savings = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=constants.DEFAULT_CURRENCY,
        blank=True,
        null=True
    )
    monobank_token = models.CharField(max_length=255, default="")
