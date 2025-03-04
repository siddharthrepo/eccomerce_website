from django.shortcuts import render , redirect
from .forms import VendorRegistrationForm  , VendorLoginForm
from .models import Vendor
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login , logout
from  store.models import Product


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
        initial_data = {"vendor_name":"" , "store_name":"" , "email":"" , "phone_number":"" , "address":""}
        form = VendorRegistrationForm(initial=initial_data)

    return render(request, 'vendor/register.html', {'form': form})

def vendor_login_view(request):
    if request.method == 'POST':
        form = VendorLoginForm(data=request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if a Vendor with this email exists and has an associated User
            try:
                vendor = Vendor.objects.get(email=email)
                
                if vendor.user:  # Ensure Vendor is linked to a User
                    user = authenticate(request, username=vendor.user.username, password=password)
                    
                    if user is not None:
                        if vendor.is_active:
                            login(request, user)  # Log in the user
                            request.session['vendor_id'] = str(vendor.id)  # Track Vendor ID in session
                            messages.success(request, "Login successful!")
                            return redirect('product_management')  # Redirect to vendor dashboard
                        else:
                            messages.error(request, "This vendor account is inactive.")
                    else:
                        messages.error(request, "Invalid password.")
                else:
                    messages.error(request, "No user account associated with this vendor.")
            
            except Vendor.DoesNotExist:
                messages.error(request, "No vendor found with this email.")
        
        else:
            messages.error(request, "Please correct the errors below.")
    
    else:
        initial_data = {"email":""}
        form = VendorLoginForm(initial=initial_data)

    return render(request, 'vendor/login.html', {'form': form})


def vendor_logout_view(request):
    # Log out the user (clear session and deactivate user)
    logout(request)
    
    # Clear any vendor-specific session data
    if 'vendor_id' in request.session:
        del request.session['vendor_id']
    
    # Optionally, you can add a message to inform the vendor they are logged out
    messages.success(request, "You have been logged out successfully.")
    
    # Redirect the vendor to the login page (or home page)
    return redirect('vendor_login')



@login_required
def product_management(request):
    print(request.user)
    try:
        vendor = Vendor.objects.get(email=request.user)  # Adjust field as needed
        print(vendor)
    except Vendor.DoesNotExist:
        return render(request, "vendor/404.html")  # Redirect if the user is not a vendor

    if request.method == "POST":
        # You could add code here to handle form submission for adding products
        pass
    
    # Render the template with the vendor's products
    products = Product.objects.filter(vendor = vendor)[:50]
    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "vendor/ProductManagement.html", context)

from .forms import ProductForm
@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Associate with logged-in vendor (update with your logic)
            if request.user.is_authenticated and hasattr(request.user, 'vendor'):
                product.vendor = request.user.vendor
            product.save()
            return redirect('product_management')  # Replace with your vendor dashboard URL name
    else:
        form = ProductForm()

    return render(request, 'vendor/addProduct.html', {'form': form})
