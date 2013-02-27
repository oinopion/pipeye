from django import forms
from .models import User


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'preferred_mailout_time')
