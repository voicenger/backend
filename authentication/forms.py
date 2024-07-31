from django import forms
from .models import Profile

# Form for updating the Profile model
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Specifies the fields to include in the form
        fields = ['picture', 'nickname', 'phone_number', 'age', 'status']
