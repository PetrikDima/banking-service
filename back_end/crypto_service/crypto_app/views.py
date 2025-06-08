import json

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.crypto_exchanges_scraper import CryptoPriceFetcher


class Top5CryptosListView(APIView):

    def get(self, request):
        cache_key = 'top_5_cryptos'
        cached_data = cache.get(cache_key)
        ttl_seconds = 60 * 60  # 1 година
        if cached_data:
            crypto_data = json.loads(cached_data)
        else:
            fetcher = CryptoPriceFetcher()
            crypto_data = fetcher.get_top_5_cryptos_with_prices()
            if crypto_data:
                cache.set(cache_key, json.dumps(crypto_data), timeout=ttl_seconds)
        return Response(crypto_data)


class MonthlyPricesListView(APIView):

    def get(self, request):
        cache_key = 'crypto_monthly_prices'
        cached_data = cache.get(cache_key)
        ttl_seconds = 60 * 60  # 1 година
        if cached_data:
            crypto_data = json.loads(cached_data)
        else:
            fetcher = CryptoPriceFetcher()
            crypto_data = fetcher.fetch_monthly_prices()
            if crypto_data:
                cache.set(cache_key, json.dumps(crypto_data), timeout=ttl_seconds)
        return Response(crypto_data)
