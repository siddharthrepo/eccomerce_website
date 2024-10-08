from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart , cartData , guestOrder

# Create your views here.
def store(request):
    
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products' : products , 'cartItems' : cartItems}
    print(request.user)
    return render(request , 'store/store.html' , context)

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

def updateItem(request):
    data = json.loads(request.body)
    print(data)
    productId = data['productId']
    action = data['action']
    print("Action :" , action)
    print("productid :" , productId)

    customer = request.user.customer 
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer= customer , complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order=order , product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added' , safe=False)


# in incognito mode csrf token is not generated , a quick fix for that is 
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete=False)
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order =order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
    else:
        customer, order = guestOrder(data , request)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    return JsonResponse('Payment complete !:' , safe=False)


def send_total_to_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        cartItems = order.get_cart_items
        
    else:
        cookieData = cookieCart(request)
        cartItems =  cookieData['cartItems']
        
    context = {'cartItems':cartItems }
    return JsonResponse(context)
