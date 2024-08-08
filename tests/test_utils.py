import pytest
from unittest.mock import patch
from django.core.exceptions import ValidationError
from voicengerapp.utils import google_get_access_token, google_get_user_info

@pytest.mark.django_db
def test_google_get_access_token_success():
    with patch('requests.post') as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {'access_token': 'dummy_access_token'}

        token = google_get_access_token(code='dummy_code', redirect_uri='http://testserver/google')
        assert token == 'dummy_access_token'

@pytest.mark.django_db
def test_google_get_access_token_failure():
    with patch('requests.post') as mock_post:
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {'error_description': 'Invalid code'}

        with pytest.raises(ValidationError):
            google_get_access_token(code='invalid_code', redirect_uri='http://testserver/google')
