from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RoomSerializer, MessageSerializer, TransportationSerializer, ProfileSerializer, RegisterSerializer, ClientsSerializer, ProductSerializer, DeliverySerializer, DeliveryListsSerializer, RiderSerializer
from .models import Profile, Products, Delivery, Transportation, Message, Room
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import DestroyAPIView
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView
from rest_framework import status as drf_status
from django.contrib.auth import get_user_model

User = get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
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
            "id": self.user.id,
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
        username = request.data.get("username")

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "This mobile number is already registered."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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


class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class SubmitDeliveryView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, user_id, product_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        delivery_data = {
            'customer': user.id,
            'products': product.id,
            'rider': request.data.get('rider', ''),
            'location': request.data.get('location', ''),
            'delivery_issued': request.data.get('delivery_issued', ''),
        }

        serializer = DeliverySerializer(data=delivery_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeliveriesView(generics.ListAPIView):
    serializer_class = DeliveryListsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Delivery.objects.filter(customer_id=user_id)



class RidersListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RiderSerializer



class UpdateUserStatusView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)

        new_status = request.data.get('status')
        if not new_status:
            return Response({"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)

        profile.status = new_status
        profile.save()

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteUserView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, userid):
        user = get_object_or_404(User, id=userid)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class DeliveryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Delivery.objects.all()
    serializer_class = DeliveryListsSerializer


class UpdateDeliveryStatusView(generics.UpdateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "delivery_id"

    def update(self, request, *args, **kwargs):
        delivery = get_object_or_404(Delivery, id=kwargs.get(self.lookup_url_kwarg))
        serializer = self.get_serializer(delivery, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # ✅ return fresh serialized object after update
        return Response(self.get_serializer(delivery).data, status=status.HTTP_200_OK)

class DeleteDeliveryView(generics.DestroyAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "delivery_id"

    def delete(self, request, *args, **kwargs):
        delivery = get_object_or_404(Delivery, id=kwargs.get(self.lookup_url_kwarg))
        delivery.delete()
        return Response({"message": "Delivery deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class TransportationCreateView(generics.CreateAPIView):
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.kwargs['user_id']
        return context


class CustomerTransportationListView(generics.ListAPIView):
    serializer_class = TransportationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        customer = get_object_or_404(User, id=customer_id)
        return Transportation.objects.filter(customer=customer).order_by('-id')



class TransportMapView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, transportation_id):
        try:
            transportation = Transportation.objects.get(id=transportation_id)
        except Transportation.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        serializer = TransportationSerializer(transportation)
        return Response(serializer.data)


class TransportationUpdatePricePaymentView(generics.UpdateAPIView):
    serializer_class = TransportationSerializer
    permission_classes = [AllowAny]  # adjust as needed

    def get_object(self):
        transportation_id = self.kwargs['transportation_id']
        return get_object_or_404(Transportation, id=transportation_id)

    def update(self, request, *args, **kwargs):
        transportation = self.get_object()
        data = {}

        if 'price' in request.data:
            data['price'] = request.data['price']
        if 'payment' in request.data:
            data['payment'] = request.data['payment']

        serializer = self.get_serializer(
            transportation, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



class TransportationListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Transportation.objects.all().order_by('-date_requested')
    serializer_class = TransportationSerializer


class UpdateTransportView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, transport_id):
        transport = get_object_or_404(Transportation, id=transport_id)
        rider_name = request.data.get("rider")

        if rider_name:
            # Optional: check if such a user exists
            if not User.objects.filter(first_name=rider_name).exists():
                return Response({"error": "Rider not found"}, status=status.HTTP_404_NOT_FOUND)

            # Save only the text (not a User object)
            transport.rider = rider_name

        transport.save()
        serializer = TransportationSerializer(transport)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProfileByRoleView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        role = self.kwargs.get('role')
        return Profile.objects.filter(role=role).select_related('user')


class TransportationPaymentView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TransportationSerializer
    queryset = Transportation.objects.all()
    lookup_url_kwarg = "transport_id"

    def update(self, request, *args, **kwargs):
        transport = get_object_or_404(Transportation, id=self.kwargs.get("transport_id"))
        serializer = self.get_serializer(transport, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save payment image
        if "payment" in request.data:
            transport.payment = request.data["payment"]

        # Update status
        if "status" in request.data:
            transport.status = request.data["status"]

        # Update price
        if "price" in request.data:
            transport.price = request.data["price"]

        transport.save()
        return Response(TransportationSerializer(transport).data, status=drf_status.HTTP_200_OK)



class UpdateDeliveryPaymentView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, delivery_id):
        delivery = get_object_or_404(Delivery, id=delivery_id)
        serializer = DeliverySerializer(delivery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, delivery_id):
        return self.put(request, delivery_id)


class ArrivedDeliveryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DeliveryListsSerializer

    def get_queryset(self):
        return Delivery.objects.filter(status='Arrived')


class ArrivedTransportationListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TransportationSerializer

    def get_queryset(self):
        return Transportation.objects.filter(status="Arrived")


class ChatRoomView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user1_id, user2_id):
        try:
            room = Room.objects.get(user1_id=user1_id, user2_id=user2_id)
        except Room.DoesNotExist:
            try:
                room = Room.objects.get(user1_id=user2_id, user2_id=user1_id)
            except Room.DoesNotExist:
                return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def post(self, request, user1_id, user2_id):
        sender_id = request.data.get("sender_id")
        content = request.data.get("content")

        if not sender_id:
            return Response({"error": "Sender ID required"}, status=status.HTTP_400_BAD_REQUEST)
        if not content:
            return Response({"error": "Message content required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = User.objects.get(id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found"}, status=status.HTTP_404_NOT_FOUND)

        room, created = Room.objects.get_or_create(
            user1_id=min(user1_id, user2_id),
            user2_id=max(user1_id, user2_id)
        )

        message = Message.objects.create(room=room, sender=sender, content=content)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserRoomsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        rooms = Room.objects.filter(user1_id=user_id) | Room.objects.filter(user2_id=user_id)
        rooms = rooms.distinct()

        # Get the other user in each room
        user_ids = []
        for room in rooms:
            if room.user1_id == user_id:
                user_ids.append(room.user2_id)
            else:
                user_ids.append(room.user1_id)

        users = User.objects.filter(id__in=user_ids)
        data = [{"id": u.id, "first_name": u.first_name, "username": u.username} for u in users]

        return Response(data)


class ChatUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, first_name):
        try:
            users = User.objects.filter(first_name__iexact=first_name).values("id", "first_name", "username")
            if not users.exists():
                return Response({"error": "No user found with that first name"}, status=status.HTTP_404_NOT_FOUND)
            return Response(users, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)