from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Subscription(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    subscribed_at = models.DateTimeField(auto_now_add=True)
    payment_sum = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
