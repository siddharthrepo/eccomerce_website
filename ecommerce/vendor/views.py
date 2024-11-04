from django.shortcuts import render , redirect
from .forms import VendorRegistrationForm  , VendorLoginForm
from django.contrib.auth.forms  import  AuthenticationForm
from django.contrib.auth import login  , logout , authenticate
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import VendorLoginForm


def vendor_register_view(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('login_vendor')  # Replace with your login URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VendorRegistrationForm()

    return render(request, 'vendor/register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vendor
from .forms import VendorLoginForm

def vendor_login_view(request):
    if request.method == 'POST':
        form = VendorLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                vendor = Vendor.objects.get(email=email)
                if vendor.check_password(password) and vendor.is_active:
                    request.session['vendor_id'] = str(vendor.id)
                    messages.success(request, "Login successful!")
                    return redirect('store')  # Replace with your vendor dashboard or home page
                else:
                    messages.error(request, "Invalid email or password.")
            except Vendor.DoesNotExist:
                messages.error(request, "No vendor found with this email.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VendorLoginForm()

    return render(request, 'vendor/login.html', {'form': form})


from django.shortcuts import redirect
from django.contrib import messages

def vendor_logout_view(request):
    # Clear the session data to log out the vendor
    if 'vendor_id' in request.session:
        del request.session['vendor_id']
        messages.success(request, "Logout successful!")
    else:
        messages.info(request, "You are not logged in.")

    # Redirect to the login page or home page after logout
    return redirect('login_vendor')  # Replace with your desired redirect page
