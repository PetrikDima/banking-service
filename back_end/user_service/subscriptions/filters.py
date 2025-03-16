import django_filters

from .models import Subscription


class SubscriptionFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    subscribed_at = django_filters.DateFilter()
    subscribed_at__after = django_filters.DateFilter(field_name='subscribed_at', lookup_expr='gte')
    subscribed_at__before = django_filters.DateFilter(field_name='subscribed_at', lookup_expr='lte')
    payment_sum = django_filters.NumberFilter()
    payment_sum__lte = django_filters.NumberFilter(field_name='payment_sum', lookup_expr='lte')
    payment_sum__gte = django_filters.NumberFilter(field_name='payment_sum', lookup_expr='gte')
    user = django_filters.NumberFilter(field_name="user__id")

    class Meta:
        model = Subscription
        fields = ['title', 'description', 'subscribed_at', 'payment_sum', 'currency', 'user']
