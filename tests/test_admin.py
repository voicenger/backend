import pytest
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from unittest.mock import Mock
from voicengerapp.models import User
from voicengerapp.admin import UserAdmin

User = get_user_model()

@pytest.mark.django_db
class TestUserAdmin:

    @classmethod
    def setup_class(cls):
        cls.admin_site = AdminSite()
        cls.user_admin = UserAdmin(model=User, admin_site=cls.admin_site)
        cls.request_factory = RequestFactory()

    def test_list_display(self):
        assert self.user_admin.list_display == ('email', 'first_name', 'last_name', 'registration_method', 'is_active')

    def test_search_fields(self):
        assert self.user_admin.search_fields == ('email', 'first_name', 'last_name')

    def test_list_filter(self):
        assert self.user_admin.list_filter == ('registration_method', 'is_active', 'date_joined')

    def test_ordering(self):
        assert self.user_admin.ordering == ('-date_joined',)

    def test_readonly_fields(self):
        assert self.user_admin.readonly_fields == ('last_login', 'date_joined')

    def test_fieldsets(self):
        assert self.user_admin.fieldsets == (
            (None, {'fields': ('email', 'first_name', 'last_name', 'registration_method', 'password')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
            ('Dates', {'fields': ('last_login', 'date_joined')}),
        )

    def test_save_model(self):
        # Create a test user
        user = User.objects.create(email='testuser@example.com', username='testuser', password='password')
        form_data = {
            'email': 'testuser@example.com',
            'password': 'new_password123',
            'registration_method': 'email'  # Add this field to avoid errors
        }
        form = self.user_admin.get_form(self.request_factory.get('/'))(data=form_data, instance=user)
        
        # Check if form is valid and process password change
        assert form.is_valid(), form.errors
        self.user_admin.save_model(self.request_factory.get('/'), user, form, change=True)
        user.refresh_from_db()
        assert user.check_password('new_password123')

    def test_make_active(self):
        user = User.objects.create(email='inactiveuser@example.com', is_active=False)
        queryset = User.objects.filter(id=user.id)
        request = self.request_factory.get('/admin/authentication/user/')
        request._messages = Mock()  # Mock messages

        self.user_admin.make_active(request, queryset)
        user.refresh_from_db()
        assert user.is_active

    def test_make_inactive(self):
        user = User.objects.create(email='activeuser@example.com', is_active=True)
        queryset = User.objects.filter(id=user.id)
        request = self.request_factory.get('/admin/authentication/user/')
        request._messages = Mock()  # Mock messages

        self.user_admin.make_inactive(request, queryset)
        user.refresh_from_db()
        assert not user.is_active

    def test_make_active_action(self):
        assert self.user_admin.make_active.short_description == "Activate selected users"

    def test_make_inactive_action(self):
        assert self.user_admin.make_inactive.short_description == "Deactivate selected users"
