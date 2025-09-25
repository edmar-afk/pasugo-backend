# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Products, Delivery, Transportation
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


class RiderSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'is_active', 'is_staff', 'is_superuser', 'date_joined',
            'profile'
        ]
        

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
        role = validated_data.pop('role', None) or "Rider"  # fallback
        profile_picture = validated_data.pop('profile_picture', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name='Pending',
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


class DeliverySerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    products = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all())

    class Meta:
        model = Delivery
        fields = ['id', 'customer', 'rider', 'products', 'status', 'location', 'delivery_issued', 'message']
        read_only_fields = ['id']


class DeliveryListsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True)
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = ['id', 'customer', 'rider', 'products', 'status', 'location', 'message', 'delivery_issued']
        
        

class TransportationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportation
        fields = ['id', 'customer', 'date_requested', 'rider', 'status', 'current_location', 'destination', 'message', 'price', 'payment', 'passenger']
        read_only_fields = ['customer', 'status', 'rider', 'date_requested']

    def create(self, validated_data):
        user_id = self.context['user_id']
        validated_data['customer'] = User.objects.get(id=user_id)
        return super().create(validated_data)