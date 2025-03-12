from django.contrib.auth import get_user_model
from django.db import models
from djmoney.models import fields


User = get_user_model()


class Subscription(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    subscribed_at = models.DateTimeField(auto_now_add=True)
    pay_sum = fields.MoneyField(default_currency='USD', max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
