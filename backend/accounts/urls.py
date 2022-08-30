"""accounts URL Configuration. These patterns are added to backend/urls.py"""
from django.urls import path
from django.conf.urls import include

accounts_urlpatterns = [
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/register/", include("dj_rest_auth.registration.urls")),
]
