from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("register_vendor/" , views.vendor_register_view , name="register_vendor"),
    path("login_vendor/" , views.vendor_login_view , name="login_vendor"),
    path("logout_vendor/" , views.vendor_logout_view , name="logout_vendor"),
    path("product_management/" , views.product_management , name="product_management"),
    path('vendor/add-product/', views.add_product, name='add_product'),
    path('vendor/<uuid:vendor_id>/orders/', views.vendor_ordered_items, name='vendor_orders'),
    path('update_order_status/<int:order_id>/' , views.update_order_status ,name="update_order_status" ),
    path("api/vendor-orders/<uuid:vendor_id>/", views.vendor_ordered_items_api, name="vendor_orders_api"),
    path('product-inventory/<int:product_id>/', views.get_product_inventory, name="product_inventory"), 
    path('update-inventory/<int:product_id>/', views.update_inventory, name="update_inventory"),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
]
