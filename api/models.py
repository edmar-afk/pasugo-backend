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
    status = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    delivery_issued = models.TextField(blank=True, null=True)