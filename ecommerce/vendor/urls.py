from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("register_vendor/" , views.vendor_register_view , name="register_vendor"),
    path("login_vendor/" , views.vendor_login_view , name="login_vendor"),
    path("logout_vendor/" , views.vendor_logout_view , name="logout_vendor"),
    path("product_management/" , views.product_management , name="product_management"),
]
