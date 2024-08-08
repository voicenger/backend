import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch
from voicengerapp.models import User

@pytest.mark.django_db
def test_google_login_existing_user():
    client = APIClient()
    with patch('requests.post') as mock_post, patch('requests.get') as mock_get:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {'access_token': 'dummy_access_token'}
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {'email': 'test@example.com'}

        User.objects.create(email='test@example.com', username='testuser')

        response = client.get(reverse('login-with-google'), {'code': 'dummy_code'})
        assert response.status_code == 200
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data
        assert 'user' in response.data
