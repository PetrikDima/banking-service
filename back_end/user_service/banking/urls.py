from django.urls import path

from .views import MonobankPersonalInfoListView

urlpatterns = [
    path('monobank/personal-info/', MonobankPersonalInfoListView.as_view()),
]