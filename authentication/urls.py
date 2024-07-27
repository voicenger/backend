from django.urls import path, include
from . import views

urlpatterns = [
   path("auth/google/", views.GoogleLoginApi.as_view(), 
         name="login-with-google"),
   path('accounts/', include('allauth.urls')),
]