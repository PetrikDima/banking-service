from django.urls import path

from .views import Top5CryptosListView, MonthlyPricesListView

urlpatterns = [
    path('top_cryptos', Top5CryptosListView.as_view()),
    path('monthly_prices', MonthlyPricesListView.as_view()),
]