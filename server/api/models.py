from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField


class CustomUser(AbstractUser):
    currency = models.CharField(max_length=3, default="UAH")  # Валюта як текстове поле
    monthly_income = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="UAH"  # Правильний спосіб вказати валюту
    )
