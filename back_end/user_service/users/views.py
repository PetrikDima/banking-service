from django.contrib.auth.views import UserModel
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from back_end.user_service.users.serializers import CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
