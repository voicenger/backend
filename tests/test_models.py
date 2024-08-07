import pytest
from authentication.models import User

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create(
        username='testuser',
        email='test@example.com',
        registration_method='email'
    )
    assert user.email == 'test@example.com'
    assert user.registration_method == 'email'
    assert str(user) == 'testuser'
