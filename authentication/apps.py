from django.apps import AppConfig


# Configuration for the 'authentication' app
class AuthenticationConfig(AppConfig):
    # Specifies the default field type for auto-created primary keys
    default_auto_field = "django.db.models.BigAutoField"
    # Specifies the name of the app
    name = "authentication"

    def ready(self):
        # Importing signals when the app is ready
        import authentication.signals