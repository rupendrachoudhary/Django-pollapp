"""pollproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from registration import views as v
from myapp import views
from registration.views import SignUpView

urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),
    path('poll/', include('myapp.urls')),
    path("registration/", SignUpView.as_view(), name="registration"),
   # path('registration/', v.registration, name="registration"),
    path('admin/', admin.site.urls),
    #To use the auth app we need to add it to our project-level urls.py file.
    path('', include('django.contrib.auth.urls')),
]
