from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
