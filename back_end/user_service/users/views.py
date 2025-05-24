from django.contrib.auth.views import UserModel
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomUserSerializer, CustomTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class UserMonobankTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        request.user.monobank_token = token
        request.user.save()
        return Response({"success": True})

    def get(self, request, *args, **kwargs):
        return Response({"token": request.user.monobank_token})
