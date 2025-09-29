from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment

CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone", "city", "avatar"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "phone", "city"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = (
            "user",
            "stripe_product_id",
            "stripe_price_id",
            "stripe_session_id",
            "payment_url",
        )
