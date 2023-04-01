from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *


# Logout User Function
def logout_user(request):
    logout(request)
    return redirect('login')

# Login Function and Page
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.add_message(request, messages.INFO,
                                     'Wrong username or password')
                return redirect('login')
        return render(request, 'login/login.html', {})

# Displaying Home Page Function
def home(request):
    if request.user.is_authenticated:

        return render(request, 'home/home.html', {})
    else:
        return redirect('login')