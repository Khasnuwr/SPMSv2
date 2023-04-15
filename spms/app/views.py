from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *


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

# Displaying Student Wise PLO Table (ONLY Student will access it)
def studentWisePlo(request):
    if request.user.is_authenticated:
        if request.user.role == 'Student':
            return render(request, 'student/ploTable.html', {})
        else:
            return redirect('home')
    else:
        return redirect('login')

# Displaying Course Wise CO Analysis
def studentCourseWiseCO(request):
    if request.user.is_authenticated:
        if request.user.role == 'Student':
            return render(request, 'student/coCourse.html', {})
        else:
            return redirect('home')
    else:
        return redirect('login')

# Displaying CO input Form For Faculty
def gradeInputForm(request):
    if request.user.is_authenticated:
        if request.user.role == 'Faculty': 
            success = 'success'
            form = GradeInputForm()
            if request.method == 'POST':
                form = GradeInputForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.add_message(
                        request, messages.SUCCESS, 'GRADE Submission Successful')
                else:
                    success = 'danger'
                    messages.add_message(
                        request, messages.SUCCESS, 'GRADE Submission Failed!')
                        
            return render(request, 'faculty/coInputForm.html', {    'form':form,
                                                                    'courses': Course_T.objects.all(),
                                                                    'success': success})
        else:
            return redirect('home')
    else:
        return redirect('login')