from django.urls import path, include
from . import views

urlpatterns = [
   path("auth/google/", views.GoogleLoginApi.as_view(), 
         name="login-with-google"),
   path('accounts/', include('allauth.urls')),
   path('profile/', views.profile_view, name='profile'),
   path('profile/edit/', views.edit_profile, name='edit_profile'),
]