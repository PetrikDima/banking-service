"""
URL configuration for news_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi, views
from rest_framework import permissions

schema_view = views.get_schema_view(
   openapi.Info(
      title="News Service API",
      default_version="v1",
      description="API documentation for News service",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="petrikdima16@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("news_app.urls")),
    path('api/v1/news_service/swagger/', schema_view.with_ui('swagger'), name='swagger')
]
