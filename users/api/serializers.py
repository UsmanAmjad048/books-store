from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_superuser']

    def create(self, validated_data):
        if validated_data.get('is_superuser') is True:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                is_superuser=validated_data['is_superuser'],
                is_active= False,
            )
            return user

        else:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                is_superuser=validated_data['is_superuser'],
            )
            return user
