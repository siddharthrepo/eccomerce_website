from django.shortcuts import render , get_object_or_404
from django.http import JsonResponse
import json
import datetime
from itertools import groupby
from .models import *
from .utils import cookieCart , cartData , guestOrder
import random
from .chroma_utils import query_similar_products
# Create your views here.
def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    # Get featured/advertised products for carousel
    all_products = list(Product.objects.filter(image__isnull=False))
    advertised_products = random.sample(all_products, min(len(all_products), 5))

    # Get unique categories for the category icons grid
    categories = Product.objects.filter(catgory__isnull=False).values_list('catgory', flat=True).distinct()

    # Create category data with sample product image for icon
    category_data = []
    for category in categories:
        sample_product = Product.objects.filter(catgory=category, image__isnull=False).first()
        if sample_product:
            category_data.append({
                'name': category,
                'image': sample_product.imageURL,
                'product_count': Product.objects.filter(catgory=category).count()
            })

    context = {
        'cartItems': cartItems,
        'advertised_products': advertised_products,
        'categories': category_data
    }
    return render(request, 'store/simple_homepage.html', context)

def category_products(request, category_name, subcategory_name=None):
    from urllib.parse import unquote

    data = cartData(request)
    cartItems = data['cartItems']

    # URL decode the parameters to handle spaces and special characters
    category_name = unquote(category_name)
    if subcategory_name:
        subcategory_name = unquote(subcategory_name)

    # Get all subcategories for the sidebar
    subcategories = Product.objects.filter(catgory=category_name, sub_catgory__isnull=False).values_list('sub_catgory', flat=True).distinct()

    # Create subcategory data with sample product image for icon
    subcategory_data = []
    for subcategory in subcategories:
        sample_product = Product.objects.filter(catgory=category_name, sub_catgory=subcategory, image__isnull=False).first()
        if sample_product:
            subcategory_data.append({
                'name': subcategory,
                'image': sample_product.imageURL,
                'product_count': Product.objects.filter(catgory=category_name, sub_catgory=subcategory).count()
            })

    # Filter products based on subcategory if specified
    if subcategory_name:
        products = Product.objects.filter(catgory=category_name, sub_catgory=subcategory_name, image__isnull=False).order_by('name')
        current_subcategory = subcategory_name
    else:
        # Show all products if no subcategory specified
        products = Product.objects.filter(catgory=category_name, image__isnull=False).order_by('sub_catgory', 'name')
        current_subcategory = None

    context = {
        'category_name': category_name,
        'current_subcategory': current_subcategory,
        'subcategories': subcategory_data,
        'products': products,
        'cartItems': cartItems
    }
    return render(request, 'store/category_products_sidebar.html', context)

def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    context = {"items" : items , 'order':order , "cartItems":cartItems}

    return render(request , 'store/cart.html' , context)

def checkout(request):
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {"items" : items , 'order':order , "cartItems":cartItems}
   
    return render(request , 'store/checkout.html' , context)

from django.http import JsonResponse
import json
from .models import Product, Order, OrderItem

def updateItem(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    customer = request.user.customer

    print("action",action)
    print("product_id",product_id)

    # ✅ Always fetch the correct active cart
    order = Order.objects.filter(customer=customer, status="Pending").order_by('-date_ordered').first()

    if not order:
        order = Order.objects.create(customer=customer, status="Pending")

    product = Product.objects.get(id=product_id)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item updated successfully", safe=False)



# in incognito mode csrf token is not generated , a quick fix for that is 
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
from django.http import JsonResponse
import datetime
import json
from .models import Order, OrderItem, Product, ShippingAddress

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        # Fetch only the latest "Pending" order
        order = Order.objects.filter(customer=customer, status="Pending").order_by('-date_ordered').first()

        if not order:
            return JsonResponse({"error": "No active order found!"}, status=400)

        order.transaction_id = transaction_id

        # Check if the total matches
        total = float(data['form']['total'])
        if total == order.get_cart_total:
            order.complete = True
            order.status = "Delivered"  # Mark order as completed
            order.save()

            # Reduce stock for each ordered item
            order_items = order.orderitem_set.all()
            for item in order_items:
                product = item.product
                if product.inventory >= item.quantity:
                    product.inventory -= item.quantity  # Reduce stock
                    product.save()
                else:
                    return JsonResponse({"error": f"Not enough stock for {product.name}"}, status=400)

            # ✅ **Create a fresh order after checkout**
            new_order = Order.objects.create(customer=customer, status="Pending")

    else:
        customer, order = guestOrder(data, request)

    return JsonResponse("Payment complete! Cart is now empty.", safe=False)



def search_product(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched__products = Product.objects.filter(name__icontains=searched)
        return render(request , 'store/searched.html' , {"searched":searched , "products":searched__products})
    else:
        return render(request , 'store/searched.html' , {})

    

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Use the same textual representation as in your migration (or model method if available)
    query_text = f"""
        id:{product.id},
        ProductName:{product.name},
        Brand: {getattr(product, 'Brand', '')},
        Category:{product.catgory},
        SubCategory:{getattr(product, 'sub_catgory', '')},
        Description: {product.description}
    """
    similar_ids = query_similar_products(query_text, n_results=9)
    similar_ids = [int(i) for i in similar_ids if int(i) != product.id]
    recommended_products = Product.objects.filter(id__in=similar_ids)
    return render(request, 'store/product_detail.html', {'product': product , 'recommended_products' : recommended_products })
