"""
URL configuration for backend_intern project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from calender.views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('', GoogleCalendarInitView.as_view(), name='google-calendar-init'), # This is the URL that the user will visit to start the OAuth flow
    path('home/', GoogleCalendarRedirectView.as_view(), name='google-calendar-redirect'), # This is the URL that the user will be redirected to after completing the OAuth flow 
]
