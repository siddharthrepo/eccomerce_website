from django import forms
from .models import Vendor

class VendorRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Confirm Password"
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

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        vendor = super().save(commit=False)
        vendor.set_password(self.cleaned_data["password"])  # Hash the password
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
