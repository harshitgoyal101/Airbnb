from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="location_images", blank=True, null=True)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="hotel_images", blank=True, null=True)
    price = models.IntegerField()

    def __str__(self):
        return self.name