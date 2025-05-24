import time
from datetime import datetime

import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MonobankPersonalInfoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            if not request.user.monobank_token:
                return Response({"error": "Monobank token not found"}, status=400)
            monobank_response = requests.get(
                "https://api.monobank.ua/personal/client-info",
                headers={"X-Token": request.user.monobank_token},
            )
            monobank_response.raise_for_status()
            return Response(monobank_response.json())
        except requests.exceptions.RequestException:
            return Response({"error": "Failed to fetch Monobank data"}, status=502)


class MonobankPersonalInfoFromToListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account, date_from, date_to, *args, **kwargs):
        if not request.user.monobank_token:
            return Response({"error": "Monobank token not found"}, status=400)

        try:
            dt_from = datetime.strptime(date_from, "%d-%m-%Y")
            dt_to = datetime.strptime(date_to, "%d-%m-%Y")
            ts_from = int(time.mktime(dt_from.timetuple()))
            ts_to = int(time.mktime(dt_to.timetuple()))
        except ValueError:
            return Response({"error": "Invalid date format. Use DD-MM-YYYY."}, status=400)

        url = f"https://api.monobank.ua/personal/statement/{account}/{ts_from}/{ts_to}"

        try:
            response = requests.get(
                url,
                headers={"X-Token": request.user.monobank_token},
                timeout=5
            )
            response.raise_for_status()
            return Response(response.json())
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch statement: {str(e)}"}, status=502)
