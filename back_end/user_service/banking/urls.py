from django.urls import path

from .views import MonobankPersonalInfoListView, MonobankPersonalInfoFromToListView

urlpatterns = [
    path('monobank/personal-info/', MonobankPersonalInfoListView.as_view()),
    path(
    'monobank/statement/<str:account>/<str:date_from>/<str:date_to>/',
        MonobankPersonalInfoFromToListView.as_view(),
        name='monobank-statement'
    ),
]