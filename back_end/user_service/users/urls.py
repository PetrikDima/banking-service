from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import CustomTokenView, UserMonobankTokenView

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('monobank/token/', UserMonobankTokenView.as_view()),
]
