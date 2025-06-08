from rest_framework import serializers

class NewsSerializer(serializers.Serializer):
    title = serializers.CharField()
    url = serializers.URLField()
