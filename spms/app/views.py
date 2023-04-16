from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *

import pandas as pd


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

# Displaying Grade input Form For Faculty
def gradeInputForm(request):
    if request.user.is_authenticated:
        if request.user.role == 'Faculty': 
            success = 'success'
            form = GradeInputForm()
            if request.method == 'POST': 
                try:
                    student_ID = User_T.objects.get(username=request.POST['studentID'])
                    courseT = Course_T.objects.get(pk=request.POST['course'])
                    form = CourseGrade_T(
                        studentID = student_ID,
                        eduYear = request.POST['eduYear'],
                        eduSemester = request.POST['eduSemester'],
                        course = courseT,
                        section = request.POST['section'],
                        grade = request.POST['grade']
                    )
                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'GRADE Submission Successful')
                except:
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
# Import Grades from CSV file
def gradeInputFromCSV(request):
    if request.user.is_authenticated:
        if request.user.role == 'Faculty':
            success = 'success'
            if request.method == 'POST':
                csv_file = request.FILES['csv_file']
                data_frame = pd.read_csv(csv_file, index_col=False, iterator=True)
                #print(data_frame['YEAR'][0])
                try:
                    for row in data_frame:
                        print(str(row['STUDENT_ID'][0])+' '+ str(row['YEAR'][0]))
                        # student = User_T.objects.raw(
                        #         "SELECT * FROM app_user_t WHERE username=%s", [str(row['STUDENT_ID'][0])]
                        # )
                        # courseT = Course_T.objects.raw(
                        #     "SELECT * FROM course_t WHERE courseID = %s", [row['COURSE'][0]]
                        # )
                        # Need fixing ^
                        student = User_T.objects.get(username=str(row['STUDENT_ID'][0]))
                        courseT = Course_T.objects.get(pk=str(row['COURSE'][0]))
                        
                        data = CourseGrade_T(studentID=student,
                            eduYear=str(row['YEAR'][0]),
                            eduSemester=str(row['SEMESTER'][0]),
                            course=courseT,
                            section=str(row['SECTION'][0]),
                            grade=str(row['GRADE'][0])
                        )
                        data.save()
                        messages.add_message(request, messages.SUCCESS, 'GRADE Submission Successful')
                except:
                    success = 'danger'
                    messages.add_message(request, messages.SUCCESS, 'GRADE Submission Failed!')
            return render(request, 'faculty/gradeImportCSV.html', {'success': success})
        else:
            return redirect('home')
    else:
        return redirect('login')