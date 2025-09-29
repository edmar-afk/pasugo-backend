from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.TextField(blank=True, null=True)
    status = models.TextField(default="Pending")
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Payment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    pay = models.ImageField(
        upload_to='payments/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    date_issued = models.DateTimeField(auto_now_add=True)
    
    
class Products(models.Model):
    name = models.TextField( blank=True, null=True,)
    picture = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
    )
    price = models.TextField( blank=True, null=True,)
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.TextField(default='Available')
    type = models.TextField( blank=True, null=True,)
    
    
class Delivery(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.TextField(blank=True, null=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    status = models.TextField(default='Pending')
    location = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    delivery_issued = models.DateTimeField(auto_now_add=True)
    payment = models.ImageField(
        upload_to='payments/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
    )
    price = models.TextField(blank=True, null=True)

class Transportation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.TextField(blank=True, null=True)
    status = models.TextField(default='Pending')
    current_location = models.TextField(blank=True, null=True)
    destination = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    price = models.TextField(blank=True, null=True)
    passenger = models.TextField(blank=True, null=True)
    payment = models.ImageField(
        upload_to='payments/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
    )
    
    
class Room(models.Model):
    user1 = models.ForeignKey(User, related_name="room_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="room_user2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # Prevent duplicate rooms

class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)