from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *

import pandas as pd

# File Response
from django.http import FileResponse
# i/o buffer
import io
# Report lab to generate pdf
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
# Report Lab Table
from reportlab.platypus import TableStyle, SimpleDocTemplate, Image, Table

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
        if request.user.role == 'Student':
            grades = CourseGrade_T.objects.filter(studentID=request.user)
            attempted_credit = 0
            total_cum_credit = 0

            for grade in grades:
                if grade.grade == 'A':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*4.00)
                elif grade.grade == 'A-':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.70)
                elif grade.grade == 'B+':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.30)
                elif grade.grade == 'B':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.00)
                elif grade.grade == 'B-':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.70)
                elif grade.grade == 'C+':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.30)
                elif grade.grade == 'C':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.00)
                elif grade.grade == 'C-':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.70)
                elif grade.grade == 'D+':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.30)
                elif grade.grade == 'D':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.00)
                elif grade.grade == 'F':
                    #course = Course_T.objects.get(pk=grade.course)
                    #attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*0.00)
            cgpa = total_cum_credit/attempted_credit
            return render(request, 'home/home.html', {  'cgpa': round(cgpa, 2),
                                                        'earned_credit': attempted_credit})
                
        return render(request, 'home/home.html', {})
    else:
        return redirect('login')
# Student Download Transcript
def genTranscript(request):
    if request.user.is_authenticated:
        if request.user.role == 'Student':
            # Create Bytestream Buffer
            buffer = io.BytesIO()
            canv = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
            # Create text object
            textobj = canv.beginText()
            textobj.setTextOrigin(inch, inch)
            textobj.setFont('Times-Roman', 10)

            # Get object of that student ID
            student = User_T.objects.get(username=request.user.username)
            # Create Empty List of lines
            lines = []
            # Append the data in the list of lines
            lines.append("                                                                              TRANSCRIPT")
            lines.append("")
            lines.append(
                f"Student Name: {student.first_name} {student.last_name}")
            lines.append(f'Student ID: {student.username}')
            lines.append(f"Department: {student.department.departmentName}")
            lines.append(f"School: {student.department.schoolID.schoolName}")
            
            lines.append(
                '___________________________________________________________________________________________')
            lines.append(
                'COURSE ID            SEMESTER              YEAR                CREDIT            GPA            GRADE             TOTAL')
            lines.append(
                '___________________________________________________________________________________________')
            grades = CourseGrade_T.objects.filter(studentID=request.user)
            attempted_credit = 0
            total_cum_credit = 0

            for grade in grades:
                if grade.grade == 'A':
                    course = Course_T.objects.get(pk=grade.course)

                    
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*4.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  4.00                    A                  {float(int(course.creditNo)*4.00)}")
                elif grade.grade == 'A-':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.70)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  3.70                    A-                  {round(float(int(course.creditNo)*3.70), 2)}")
                elif grade.grade == 'B+':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.30)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  3.30                    B+                  {round(float(int(course.creditNo)*3.30), 2)}")
                elif grade.grade == 'B':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  3.00                    B                  {float(int(course.creditNo)*3.00)}")
                elif grade.grade == 'B-':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.70)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  2.70                    B-                  {round(float(int(course.creditNo)*2.70), 2)}")
                elif grade.grade == 'C+':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.30)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  2.30                    C+                  {round(float(int(course.creditNo)*2.30), 2)}")
                elif grade.grade == 'C':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  2.00                    C                  {float(int(course.creditNo)*2.00)}")
                elif grade.grade == 'C-':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.70)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  1.70                    C-                  {round(float(int(course.creditNo)*1.70), 2)}")
                elif grade.grade == 'D+':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.30)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  1.30                    D+                  {round(float(int(course.creditNo)*1.30), 2)}")
                elif grade.grade == 'D':
                    course = Course_T.objects.get(pk=grade.course)
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  1.00                    D                  {float(int(course.creditNo)*1.00)}")
                elif grade.grade == 'F':
                    #course = Course_T.objects.get(pk=grade.course)
                    #attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*0.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  0.00                    F                  {float(int(course.creditNo)*0.00)}")
            cgpa = total_cum_credit/attempted_credit
            lines.append(
                '___________________________________________________________________________________________')
            lines.append(f"TOTAL: {round(total_cum_credit, 2)}")
            lines.append(f"ATTEMPTED CREDIT: {attempted_credit}")
            lines.append(f"CGPA: {round(cgpa, 2)}")
            # lines.append(
            #     f'Registered Vehicle Owner: {owner.registered_vehicle_owner}')
            # lines.append(
            #     f'registered Vehicle Owner ID: {owner.registered_owner_id}')
            # lines.append(
            #     f"Registered Owner's Address: {owner.registered_owner_address}")
            # lines.append(
            #     f"Registered Vehicle Owner's DOB: {owner.registered_owner_dob}")
            # lines.append(
            #     f"Registration Date: {owner.registered_owner_data_create}")
            # lines.append('')
            # lines.append(
            #     '_________________________________________________________________________________________')
            # lines.append(f"Registered Owned Vehicle(s)")
            # lines.append(
            #     '_________________________________________________________________________________________')

            # vehicles = vehicle_license_plate_registration_table.objects.filter(
            #     registered_owner_id__pk=owner_id)

            # if vehicles:
            #     for vehicle in vehicles:
            #         lines.append(f"City Name: {vehicle.city_name}")
            #         lines.append(
            #             f"Vehicle Classification: {vehicle.vehicle_classification}")
            #         lines.append(f"VIN: {vehicle.vin}")
            #         lines.append(f"Engine CC: {vehicle.engine_cc}")
            #         lines.append(f"Vehicle Brand: {vehicle.vehicle_brand}")
            #         lines.append(
            #             f"Vehicle Registered To: {vehicle.registered_owner_id.registered_vehicle_owner}")
            #         lines.append('')
            #     lines.append(
            #         '_________________________________________________________________________________________')
            # else:
            #     lines.append(
            #         f"{owner.registered_vehicle_owner} has no Registered Vehicle(s)")
            #     lines.append(
            #         '_________________________________________________________________________________________')
            # lines.append(f"Printed by {request.user}")
            # Putting lines in text object
            for line in lines:
                textobj.textLine(line)
            canv.drawText(textobj)
            canv.showPage()
            canv.save()
            buffer.seek(0)

            # Return the generated pdf file
            return FileResponse(buffer, as_attachment=True, filename=f'transcripts_of_{student.username}.pdf')
        else:
            return redirect('home')
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
                        
            return render(request, 'faculty/gradeInputForm.html', {    'form':form,
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