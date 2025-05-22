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
