import pytest
from datetime import datetime, timedelta
from voicengerapp.models import User
from voicengerapp.serializers import  UserSerializer

@pytest.mark.django_db
def test_validate_date_of_birth_future_data():
    # Тест проверяет, что дата рождения в будущем вызывает ошибку валидации.
    future_date = datetime.now() + timedelta(days=10)
    serializer = UserSerializer(data={'date_of_birth': future_date})
    assert not serializer.is_valid()
    assert 'date_of_birth' in serializer.errors
    assert serializer.errors['date_of_birth'][0] == "The date of birth cannot be in the future."

@pytest.mark.django_db
def test_validate_email_already_exist():
    # Тест проверяет, если email уже существует в БД, сериализатор вернет ошибку.
    User.objects.create(username='exist_user', email='test@gmail.com')
    serializer = UserSerializer(data={'email': 'test@gmail.com'})
    assert not serializer.is_valid()
    assert 'email' in serializer.errors
    assert serializer.errors['email'][0] == "A user with this email already exist."

@pytest.mark.django_db
def test_validate_email_unique():
    # Тест проверяет, что уникальный email ( которого еще нет в БД ) успешно проходит валидацию.
    serializer = UserSerializer(data={
        'email': 'unique@gmail.com',
        'username': 'uniqueuser',
        'password': 'testpassword123'
    })
    assert serializer.is_valid()

@pytest.mark.django_db
def test_validate_bio_too_long():
    # Тест проверяет, если больше 500 символов в bio то будет ошибка валидации.
    long_bio = 'a' * 501
    serializer = UserSerializer(data={'bio': long_bio})
    assert not serializer.is_valid()
    assert 'bio' in serializer.errors
    assert serializer.errors['bio'][0] == "Bio cannot be longer than 500 characters."

@pytest.mark.django_db
def test_validate_bio_valid_length():
    # Тест проверяет, что поле bio длиной до 500 символов проходит успешно валидацию.
    valid_bio = 'a' * 500
    serializer = UserSerializer(data={
        'bio': valid_bio,
        'username': 'validuser',
        'password': 'validpassword123'
    })
    assert serializer.is_valid()


@pytest.mark.django_db
def test_validate_username_already_exist():
    # Тест проверяет, что username является уникальным
    User.objects.create(username='exist_user', email='exist_user@gmail.com', password='password123')
    serializer = UserSerializer(data={
        'username': 'exist_user',
        'email': 'new_email@gmail.com',
        'password': 'password123'
    })

    # Проверяем, что сериализатор не валиден и вызывает ошибку с кодом 'unique'
    assert not serializer.is_valid()
    assert 'username' in serializer.errors
    assert serializer.errors['username'][0].code == 'unique'