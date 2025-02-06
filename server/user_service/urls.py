from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user_service import views

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('/', include(router.urls)),
    path('/login/', TokenObtainPairView.as_view()),
    path('/login/refresh/', TokenRefreshView.as_view()),
]
