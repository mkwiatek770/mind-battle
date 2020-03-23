from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    def create(self, validated_data: dict) -> User:
        validated_data.pop('re_password')
        user = User.objects.create(**validated_data)
        return user

    def validate(self, data: dict) -> dict:
        if not data['re_password'] == data['password']:
            raise serializers.ValidationError("Passwords don't match.")
        return data

    def validate_age(self, value: int) -> int:
        if value <= 13:
            raise ValueError("You're too young to register.")
        return value

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 're_password', 'email', 'age')
        read_only_fields = ('id',)
