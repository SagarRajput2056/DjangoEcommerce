from django import forms
from django.utils.translation import gettext_lazy as _
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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email address is already in use."))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError(_("Password must be at least 8 characters long."))
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = self.cleaned_data['is_vendor']
        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.is_vendor = self.cleaned_data['is_vendor']
            profile.save()
        return user