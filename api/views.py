from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import ProfileSerializer, RegisterSerializer, ClientsSerializer, ProductSerializer
from .models import Profile, Products
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
import os
import tempfile
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from docx2pdf import convert
from urllib.parse import urlparse
from django.conf import settings
import traceback
from rest_framework.generics import DestroyAPIView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "is_staff": self.user.is_staff,
            "is_superuser": self.user.is_superuser,
        })
        return data



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class UserProfileView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):
        profile = get_object_or_404(Profile, user__id=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ClientsListView(generics.ListAPIView):
    serializer_class = ClientsSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Profile.objects.select_related('user').all()
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        return queryset
    

class ProductCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    

class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Products.objects.all().order_by('-date_posted')
    serializer_class = ProductSerializer
    
class ProductDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    parser_classes = (MultiPartParser, FormParser)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    
    
class ProductDeleteView(DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Products.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)