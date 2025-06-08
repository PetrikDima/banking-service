from rest_framework import serializers


class Top5CryptosSerializer(serializers.Serializer):
    price = serializers.FloatField()
    trade_link = serializers.URLField()


class PriceEntrySerializer(serializers.Serializer):
    date = serializers.DateField()
    price = serializers.FloatField()


class CryptoPricesSerializer(serializers.Serializer):
    prices = serializers.DictField(
        child=PriceEntrySerializer(many=True)
    )
