from django.shortcuts import render
from .models import Hotel, Location

# Create your views here.
def get_location_detials(request, location_name):
    location = Location.objects.get(name__iexact=location_name)
    hotels = Hotel.objects.filter(location__name__iexact=location_name)
    context = {
        "location": location,
        "hotels": hotels
    }
    return render(request, "hotel/location_details.html", context=context)

def get_location_detials_by_name(request):
    kwargs = dict(request.GET)
    print(kwargs.get("city")[0])
    location = Location.objects.get(name__iexact=kwargs.get("city")[0])
    hotels = Hotel.objects.filter(location__name__iexact=kwargs.get("city")[0])
    context = {
        "location": location,
        "hotels": hotels
    }
    return render(request, "hotel/location_details.html", context=context)

def get_hotel_detials(request, hotel_name):
    hotel = Hotel.objects.get(name__iexact=hotel_name)
    location_name = hotel.location.name
    related_hotels = Hotel.objects.filter(location__name=location_name).exclude(name__iexact=hotel_name)
    context = {
        "hotel": hotel,
        "location_name": location_name,
        "hotels": related_hotels
    }
    return render(request, "hotel/hotel_details.html", context=context)