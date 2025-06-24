from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('' , views.store , name="store"),
    path('category/<str:category_name>/', views.category_products, name="category_products"),
    path('category/<str:category_name>/<str:subcategory_name>/', views.category_products, name="subcategory_products"),
    path('cart/' , views.cart , name="cart"),
    path('checkout/' , views.checkout , name="checkout"),
    path('update_item/' , views.updateItem , name="update_item"),
    path('process_order/' , views.processOrder , name="process_order"),
    path('search/' , views.search_product , name="search"),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('order-history/', views.order_history, name='order_history'),
    path('profile/', views.customer_profile, name='customer_profile'),

]
