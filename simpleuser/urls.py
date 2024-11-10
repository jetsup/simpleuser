"""
URL configuration for simpleuser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from myuser.views import(
    register_view,login_view,welcome_view,logout_view,profile_view,about_view,booking_view,base_view,
    end_booking,search_user
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register_view,name='register'),
    path('',login_view,name='login'),
    path('welcome/',welcome_view,name='welcome'),
    path('logout/',logout_view,name='logout'),
    path('profile/',profile_view,name='profile'),
    path('about/',about_view,name='about'),
    path('booking/',booking_view,name='booking'),
    path('base/',base_view,name='base'),
    path('endbooking/<int:slot_id>/',end_booking,name='endbooking'),
    # Web API endpoints
    path("search-user", search_user, name="searchuser"),
]
