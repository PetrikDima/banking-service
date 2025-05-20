from django.contrib.auth.views import UserModel
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomUserSerializer, CustomTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
