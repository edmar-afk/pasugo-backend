# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Products
from django.db import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined']



class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'email', 'role', 'status', 'profile_picture']



class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'role', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        profile_picture = validated_data.pop('profile_picture', None)

        user = User.objects.create_user(
            username=validated_data['username'],  # stores mobile number
            first_name=validated_data.get('first_name', ''),
            last_name='Pending',  # <-- Added this line
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        Profile.objects.create(
            user=user,
            role=role,
            profile_picture=profile_picture
        )

        return user


class ClientsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'status', 'profile_picture']
        


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'picture', 'date_posted', 'status', 'price', 'type']
        read_only_fields = ['id', 'date_posted']  # ✅ removed status

