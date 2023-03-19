from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    long_description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to="location_images", blank=True, null=True)

    def __str__(self):
        return self.short_description

class Hotel(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    index = models.CharField(max_length=3)
    description = models.TextField()
    short_description = models.CharField(max_length=50, blank=True, null=True)
    host_description = models.CharField(max_length=50, blank=True, null=True)
    long_description = models.TextField(null=True)
    image = models.ImageField(upload_to="hotel_images", blank=True, null=True)
    price = models.IntegerField()

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)





