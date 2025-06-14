import time
from datetime import datetime

import requests
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils.categorizer import Categorizer


class MonobankPersonalInfoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            cache_key = f'monobank_client_info_{request.user.id}'
            ttl_seconds = 60
            if cached_data := cache.get(cache_key):
                data = cached_data
            else:
                if not request.user.monobank_token:
                    return Response({"error": "Monobank token not found"}, status=400)
                raw_token = request.user.monobank_token

                if isinstance(raw_token, bytes):
                    raw_token = raw_token.decode("utf-8")

                token = raw_token.strip()
                response = requests.get(
                    "https://api.monobank.ua/personal/client-info",
                    headers={"X-Token": token},
                )
                response.raise_for_status()
                data = response.json()
                cache.set(cache_key, data, ttl_seconds)
            return Response(data)
        except requests.exceptions.RequestException:
            return Response({"error": f"Failed to fetch Monobank data\n"
                                      f"monobank response: {response}\n"
                                      f"mono token: {request.user.monobank_token}"}, status=502)


class MonobankPersonalInfoFromToListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account, date_from, date_to, *args, **kwargs):
        if not request.user.monobank_token:
            return Response({"error": "Monobank token not found"}, status=400)

        try:
            raw_token = request.user.monobank_token
            if isinstance(raw_token, bytes):
                raw_token = raw_token.decode("utf-8")

            token = raw_token.strip()
            dt_from = datetime.strptime(date_from, "%d-%m-%Y")
            dt_to = datetime.strptime(date_to, "%d-%m-%Y")
            ts_from = int(time.mktime(dt_from.timetuple()))
            ts_to = int(time.mktime(dt_to.timetuple()))
        except ValueError:
            return Response({"error": "Invalid date format. Use DD-MM-YYYY."}, status=400)

        url = f"https://api.monobank.ua/personal/statement/{account}/{ts_from}/{ts_to}"

        try:
            cache_key = f'monobank_statement_{request.user.id}_{account}_{ts_from}_{ts_to}'
            ttl_seconds = 60
            if cached_data := cache.get(cache_key):
                data = cached_data
            else:
                response = requests.get(
                    url,
                    headers={"X-Token": token},
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()
                cache.set(cache_key, data, ttl_seconds)

            if request.query_params.get("category"):
                data = Categorizer.categorize(data)

            return Response(data)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch statement: {str(e)}"}, status=502)
