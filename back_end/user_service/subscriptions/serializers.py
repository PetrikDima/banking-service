from rest_framework import serializers

from back_end.user_service.subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['title', 'description', 'subscribed_at', 'pay_sum']
