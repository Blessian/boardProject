from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_staff', 'is_active']
        read_only_fields = ['is_staff', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }
