import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print("Cart :"  , cart)
    items = []
    order = {"get_cart_items":0 , "get_cart_total":0 , "shipping":False}
    cartItems = order['get_cart_items']
    for i in cart:
        try:    
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product' :{
                    'id' : product.id,
                    'name': product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {"items" : items , 'order':order , "cartItems":cartItems}

def cartData(request):
    if request.user.is_authenticated:  
        try:
            customer = request.user.customer
            order = Order.objects.filter(customer=customer, status="Pending").order_by('-date_ordered').first()

            if order:
                items = order.orderitem_set.all()
                cartItems = order.get_cart_items 
            else:
                order = Order.objects.create(customer=customer, status="Pending")
                items = []
                cartItems = 0 
        except Exception as e:
            # if vendor logs in the main store page
            print('ran into exception' , e )
            order = 0
            items = 0   
            cartItems = 0
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    return {"items" : items , 'order':order , "cartItems":cartItems}

def guestOrder(data , request):
    print("User is not logged in...")
    print('COOKIES:' , request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer = customer,
        complete = False,
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity = item['quantity']
        )
    
    return customer, order
