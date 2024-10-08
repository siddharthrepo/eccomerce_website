from django.shortcuts import render , redirect
from django.contrib.auth.forms  import UserCreationForm, AuthenticationForm
from django.contrib.auth import login  , logout
from store.models import *
from .forms import CustomUserCreationForm

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user, name=user.username, email=user.email)
            # login(request , user)
            return redirect('login')
            # return render(request , 'authen/login.html' , )
    else:
        initial_data = {'username':'' ,'email':'' ,'password1':'' , 'password2' : '' }
        form = CustomUserCreationForm(initial = initial_data)
    return render(request , 'authen/register.html' , {"form" : form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request , data = request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request , user)
            return redirect('store')
        else:
            text = "404 : user not found"
            return render(request , 'authen/404.html' , {"text" : text})
    else:
        print("something here")
        initial_data = {'username':'' , 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request , 'authen/login.html' , {'form':form})


def logout_view(request):
    logout(request)
    return redirect('store')
