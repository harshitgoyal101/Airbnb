from django.shortcuts import render, redirect
from hotel.models import Location
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    locations = Location.objects.all()
    return render(request, "core/index.html", context={"locations": locations})

def about_us(request):
    return render(request, "core/about.html")

def team(request):
    profiles = []
    for user in User.objects.all():
        profile = UserProfile.objects.get(user=user)
        url = profile.image.url if profile.image else None
        profiles.append({
            "username": user.username,
            "image": profile.image,
            "url": url,
            "bio": profile.description
        })
    return render(request, "core/team.html", context={"profiles": profiles})

def register(request, **kwargs):
    if request.user.is_authenticated:
        return redirect('index') 
    if request.method == 'POST':
        data = request.POST
        name = data.get("name")
        email = data.get("email").lower()
        password = data.get("password")
        retry_password = data.get("retry_password")
        if password != retry_password:
            messages.error(request, 'password not match')
            return redirect('register') 
        else:
            user = User.objects.filter(email=email)
            if user:
                messages.error(request, 'email already registor')
                return redirect('register') 
            user = User.objects.create(username=name, email=email)
            user.set_password(password)
            messages.success(request, 'user created')
            return redirect('index') 
    return render(request, "core/register.html")


def login_handle(request, **kwargs):
    if request.user.is_authenticated:
        return redirect('index') 
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = User.objects.get(email=email.lower()).username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'login successful')
            return redirect('index') 
        else:
            messages.error(request, 'login failed')
            return render(request, "core/login.html")
    return render(request, "core/login.html")

def logout_view(request):
    logout(request)
    return redirect('index') 


def profile(request):
    if not request.user.is_authenticated:
        return redirect('index') 
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        bio = request.POST['bio']
        profile.description = bio
        if request.FILES:
            profile_pic = request.FILES['name']
            print(profile_pic)
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name.replace(" ","_"), profile_pic)
            uploaded_file_url = fs.url(filename)
            profile.image = uploaded_file_url.replace("/media/","")
            print(uploaded_file_url)
        profile.save()
        return redirect('profile')
    context = {
        "user": request.user,
        "profile": profile
    }
    return render(request, "core/profile.html", context=context)