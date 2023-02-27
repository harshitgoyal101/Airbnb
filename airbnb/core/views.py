from django.shortcuts import render, redirect
from hotel.models import Location
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    locations = Location.objects.all()
    return render(request, "core/index.html", context={"locations": locations})

def about_us(request):
    return render(request, "core/about.html")

def registor(request, **kwargs):
    retry_password = "23"
    if request.method == 'POST':
        data = request.POST
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        retry_password = data.get("retry_password")
        if password != retry_password:
            messages.error(request, 'password not match')
            return redirect('registor') 
        else:
            User.objects.create(username=name, email=email, password=password)
            messages.success(request, 'user created')
            return redirect('index') 
    return render(request, "core/registor.html", context=kwargs)