from rest_framework import serializers

from user_service.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="country.code")
    phone_number = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "currency",
            "country",
            "phone_number",
            "monthly_income",
            "financial_goal",
            "savings",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['first_name'] = representation['first_name'].title()
        representation['last_name'] = representation['last_name'].title()

        return representation
