from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import SubscriptionFilter
from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscribeView(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SubscriptionFilter
    search_fields = ['title', 'description', 'user']
    ordering = ['subscribed_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, currency=self.request.user.currency)
