from django.shortcuts import render , redirect , get_object_or_404
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


from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q

def product_management(request):
    try:
        vendor = Vendor.objects.get(email=request.user.email)  
    except Vendor.DoesNotExist:
        return render(request, "vendor/404.html") 

    query = request.GET.get("search", "")
    page_number = request.GET.get("page", 1)  # Get current page from request
    per_page = 10  # Adjust the number of products per page

    # Apply filtering before pagination
    products = Product.objects.filter(vendor=vendor)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(catgory__icontains=query)
        )

    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(catgory=category_filter)

    inventory_filter = request.GET.get('inventory', '')
    if inventory_filter == 'low':
        products = products.filter(inventory__lte=10, inventory__gt=0)  # Low stock
    elif inventory_filter == 'out':
        products = products.filter(inventory=0) 

    # Paginate results
    paginator = Paginator(products, per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        "vendor": vendor,
        "products": page_obj,  # Send paginated object to template
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


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import  Vendor
from store.models import OrderItem
from .serializers import OrderItemSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_ordered_items_api(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
        ordered_items = OrderItem.objects.filter(product__vendor=vendor).select_related('product', 'order', 'order__customer')

        # Serializing data
        response_data = {
            "vendor": vendor.vendor_name,
            "ordered_items": []
        }

        for item in ordered_items:
            response_data["ordered_items"].append({
                "id": item.id,
                "order_id": item.order.id if item.order else None,
                "customer_name": item.order.customer.name if item.order and item.order.customer else "Guest",
                "product_name": item.product.name,
                "order_status": item.order.status if item.order else "N/A",
                "quantity": item.quantity,
                "date_added": item.date_added.strftime("%Y-%m-%d %H:%M:%S")
            })
        return Response(response_data, status=200)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=404)
    
from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from .models import Vendor
from store.models import OrderItem

def vendor_ordered_items(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    # Fetch ordered items for the vendor
    ordered_items = (
        OrderItem.objects.filter(product__vendor=vendor)
        .select_related("product", "order", "order__customer")
        .order_by("-order__date_ordered")  # Sort newest first
    )

    # Properly grouping orders
    orders_grouped = defaultdict(lambda: {"order": None, "items": []})

    for item in ordered_items:
        order = item.order
        order_id = order.id if order else None

        if orders_grouped[order_id]["order"] is None:
            orders_grouped[order_id]["order"] = order

        orders_grouped[order_id]["items"].append({
            "id": item.id,
            "order_id": order.id if order else None,
            "customer_name": order.customer.name if order and order.customer else "Guest",
            "product_name": item.product.name,
            "order_status": order.status if order else "N/A",
            "quantity": item.quantity,
            "date_added": item.date_added.strftime("%Y-%m-%d %H:%M:%S"),
        })

    context = {
        "vendor": vendor,
        "orders_grouped": dict(orders_grouped)
    }   
    return render(request, "vendor/orders.html", context)

def get_product_inventory(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse({"inventory": product.inventory})

def update_inventory(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        new_inventory = request.POST.get('inventory')
        if new_inventory.isdigit():
            product.inventory = int(new_inventory)
            product.save()
            return redirect('product_management')  # Change to your actual dashboard view
    
    return render(request, "vendor/update_inventory.html", {'product': product})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from store.models import OrderItem, Order
from .models import Vendor

@csrf_exempt  # Temporarily disabling CSRF for demo purposes (use proper authentication in production!)
def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")

        if new_status in ["Pending", "Out for delivery", "Delivered"]:
            order.status = new_status
            order.save()
            return JsonResponse({"message": "Order status updated successfully", "status": new_status})
        else:
            return JsonResponse({"error": "Invalid status"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)