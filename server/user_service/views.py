from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from user_service.models import CustomUser
from user_service.serializers import CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
