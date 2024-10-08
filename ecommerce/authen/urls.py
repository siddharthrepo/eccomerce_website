from django.contrib import admin
from django.urls import path
from authen import views

urlpatterns = [
    path('register/' , views.register_view , name="register"),
    path('login/' , views.login_view , name="login"),
    path('logout/' , views.logout_view , name="logout"),

]
