from django import forms
from .models import Vendor
from django.contrib.auth.models import User

class VendorRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password",
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Confirm Password",
        required=False
    )

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'store_name', 'email', 'phone_number', 'address', 'profile_image']
        widgets = {
            'vendor_name': forms.TextInput(attrs={'placeholder': 'Vendor Name'}),
            'store_name': forms.TextInput(attrs={'placeholder': 'Store Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        vendor = super().save(commit=False)

        # If a password was entered, create a User instance
        password = self.cleaned_data.get("password")
        if password:
            user = User(
                username=self.cleaned_data["email"],  # or other unique field for username
                email=self.cleaned_data["email"]
            )
            user.set_password(password)
            if commit:
                user.save()
            vendor.user = user  # Link Vendor to User
        
        if commit:
            vendor.save()

        return vendor


from django import forms

class VendorLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=200,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password"
    )
