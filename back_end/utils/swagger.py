from django.urls import path
from drf_yasg import openapi, views
from rest_framework import permissions

schema_view = views.get_schema_view(
   openapi.Info(
      title="Finance Management API",
      default_version="v1",
      description="API documentation for the Finance Management application",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="petrikdima16@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   path('swagger/', schema_view.with_ui('swagger'), name='swagger')
]
