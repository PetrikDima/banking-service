from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="country.code", required=False)
    phone_number = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "currency",
            "country",
            "phone_number",
            "monthly_income",
            "financial_goal",
            "savings",
            "monobank_token",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['first_name'] = representation['first_name'].title()
        representation['last_name'] = representation['last_name'].title()
        return representation

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class CustomTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        self.user = user
        return super().validate(attrs)
