import json

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import NewsSerializer
from .utils.finance_news_scraper import FinanceNewsScraper


class NewsListView(APIView):

    def get(self, request):
        cache_key = 'news'
        cached_data = cache.get(cache_key)
        ttl_seconds = 60 * 30  # 30 хвилин

        if cached_data:
            news_data = json.loads(cached_data)
        else:
            scraper = FinanceNewsScraper()
            scraper.scrape_news()
            news_data = scraper.as_list()
            cache.set(cache_key, json.dumps(news_data), timeout=ttl_seconds)

        serializer = NewsSerializer(news_data, many=True)
        return Response(serializer.data)
