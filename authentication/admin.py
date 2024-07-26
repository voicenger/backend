from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdmin(admin.ModelAdmin):
    """
    Admin interface for the User model with extended features and configurations.
    """
    list_display = ('email', 'first_name', 'last_name', 'registration_method', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('registration_method', 'is_active', 'date_joined')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'registration_method', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def save_model(self, request, obj, form, change):
        """
        Override save_model to hash the password if it's changed.
        """
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        """
        Custom action to activate selected users.
        """
        queryset.update(is_active=True)
        self.message_user(request, "Selected users have been activated.")
    make_active.short_description = "Activate selected users"

    def make_inactive(self, request, queryset):
        """
        Custom action to deactivate selected users.
        """
        queryset.update(is_active=False)
        self.message_user(request, "Selected users have been deactivated.")
    make_inactive.short_description = "Deactivate selected users"

admin.site.register(User, UserAdmin)
