from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('' , views.store , name="store"),
    path('cart/' , views.cart , name="cart"),
    path('checkout/' , views.checkout , name="checkout"),
    path('update_item/' , views.updateItem , name="update_item"),
    path('process_order/' , views.processOrder , name="process_order"),
    path('api/data/' , views.send_total_to_cart , name="send_total_to_cart"),
    path('search/' , views.search_product , name="search"),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),

]
