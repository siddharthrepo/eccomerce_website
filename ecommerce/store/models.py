from django.db import models
from django.contrib.auth.models import User
from vendor.models import Vendor
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE ,null=True , blank=True)
    name = models.CharField(max_length=200 , null=True)
    email = models.CharField(max_length=200 , null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="products" , null=True , blank=True) 
    inventory = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7 , decimal_places=2)
    discounted_price = models.DecimalField(max_digits=7 , decimal_places=2 , null=True , blank=True)
    digital = models.BooleanField(default=False , null=True , blank=True)
    image = models.ImageField(null=True , blank=True)
    Brand = models.CharField(max_length=200 , null=True , blank=True)
    catgory = models.CharField(max_length=200 , null=True , blank=True)
    sub_catgory = models.CharField(max_length=200 , null=True , blank=True)
    description = models.CharField(max_length=10000 , null=True , blank=True)
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL , null=True , blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    STATUS = (
        ('Pending' , 'Pending'),
        ('Out for delivery' , 'out for Delivery'),
        ('Delivered' , "Delivered"),
    )
    status = models.CharField(max_length=200 , null=True,default='Pending', choices= STATUS)
    transactions_id = models.CharField(max_length=100 , null=True)
    
    def __int__(self):
        return (self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total =  sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total =  sum([item.quantity for item in orderitems])
        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL , null=True)
    order = models.ForeignKey(Order , on_delete=models.SET_NULL , null=True)
    quantity = models.IntegerField(default=0 , null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property   
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL , null=True)
    address = models.CharField(max_length=200 , null=False)
    city = models.CharField(max_length=200 , null=False)
    state = models.CharField(max_length=200 , null=False)
    zipcode = models.CharField(max_length=200 , null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.address)