from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    is_vendor = forms.BooleanField(label="Want to be a vendor?",required=False)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2', 'is_vendor']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = self.cleaned_data['is_vendor']
        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.is_vendor = self.cleaned_data['is_vendor']
            profile.save()
        return user