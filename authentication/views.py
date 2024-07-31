from urllib.parse import urlencode
from django.forms import ValidationError
from rest_framework import serializers, status
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .mixins import PublicApiMixin, ApiErrorsMixin
from .utils import google_get_access_token, google_get_user_info, generate_tokens_for_user
from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer
from .forms import ProfileForm

class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}/google'
        
        try:
            access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
            user_data = google_get_user_info(access_token=access_token)
        except ValidationError as e:
            params = urlencode({'error': str(e)})
            return redirect(f'{login_url}?{params}')
        except Exception as e:
            params = urlencode({'error': 'An error occurred while processing your request.'})
            return redirect(f'{login_url}?{params}')

        email = user_data.get('email')
        first_name = user_data.get('given_name', '')
        last_name = user_data.get('family_name', '')

        # Ensure the username is unique
        base_username = email.split('@')[0]
        username = base_username
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{suffix}"
            suffix += 1

        # Check if the user already exists by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create a new user
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                registration_method='google'
            )

        # Generate tokens
        access_token, refresh_token = generate_tokens_for_user(user)

        # Prepare response
        response_data = {
            'user': UserSerializer(user).data,
            'access_token': str(access_token),
            'refresh_token': str(refresh_token)
        }

        return Response(response_data, status=status.HTTP_200_OK)

# View to display the profile page
@login_required
def profile_view(request):
    # Gets the profile of the logged-in user and renders the profile.html template with the user's profile
    user = request.user
    
    profile, created = Profile.objects.get_or_create(user=user)
    
    profile_serializer = ProfileSerializer(profile)
    return JsonResponse(profile_serializer.data)

# View to edit the profile
@login_required
def edit_profile(request):
    # Checks if the request method is POST
    if request.method == 'POST':
        # Binds data to the form, including files
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        # Checks if the form is valid
        if form.is_valid():
            # Saves the form if valid
            form.save()
            # Redirects to the profile page after saving
            return redirect('profile')
    else:
        # Creates a form instance with the user's profile
        form = ProfileForm(instance=request.user.profile)
    # Renders the edit_profile.html template with the form
    return render(request, 'edit_profile.html', {'form': form})