from django.contrib import admin
from .models import Profile, Products, Delivery, Transportation

admin.site.register(Profile)
admin.site.register(Products)
admin.site.register(Delivery)
admin.site.register(Transportation)