# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .utils import COUNTRY_TIMEZONE_MAP



class CustomUserCreationForm(UserCreationForm):
    country = forms.ChoiceField(
        choices=[(country, country) for country in COUNTRY_TIMEZONE_MAP.keys()],
        required=True,
        label="Country"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'country']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                country=self.cleaned_data['country'],
                timezone=COUNTRY_TIMEZONE_MAP.get(self.cleaned_data['country'], 'UTC')
            )
        return user