from rest_framework import serializers
from .models import Payment, CustomUser


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


# ДОБАВЛЕНЫ НОВЫЕ КЛАССЫ:
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone", "city", "avatar"]
        read_only_fields = ["id"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "phone", "city"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get("phone"),
            city=validated_data.get("city"),
        )
        return user
