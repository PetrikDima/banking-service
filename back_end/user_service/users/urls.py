from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomTokenView, UserMonobankTokenView, LogoutView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenView.as_view()),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('monobank/token/', UserMonobankTokenView.as_view()),
]
