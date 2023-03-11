"""airbnb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from core.views import *
from hotel.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about', about_us, name='about'),
    path('register', register, name='register'),
    path('login', login_handle, name='login_handle'),
    path('logout', logout_view, name='logout_view'),
    path('profile', profile, name='profile'),
    path('get_location_detials/<str:location_name>/', get_location_detials, name="get_location_detials"),
    path('get_location_detials/', get_location_detials_by_name, name="get_location_detials_name"),
    path('get_hotel_detials/<str:hotel_name>/', get_hotel_detials, name="get_hotel_detials")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
