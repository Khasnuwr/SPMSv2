from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *

import pandas as pd
# Importing Datetime
import datetime
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
# Importing CSV Module
import csv
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
# FUNCTION OF GETTING STUDENT-WISE PLO
def getPLO(student):
    studentT = User_T.objects.get(username=student)
    if studentT.role != 'Student':
        return None
    plos = Assessment_T.objects.all()
    plodata = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    plodataC = [0,0,0,0,0,0,0,0,0,0,0,0]
    for plo in plos:
        print(f'PLO{plo.co.plo.ploNo} CO{plo.co.coNo} {plo.marks} {plo.studentID}')
        if plo.studentID.username == studentT.username:
            print(plo.studentID.username, studentT.username)
            # print(f'PLO{plo.co.plo.ploNo} CO{plo.co.coNo} {plo.marks} {plo.studentID}')
            if int(plo.co.plo.ploNo) == 1:
                plodata[0] += plo.marks
                plodataC[0]+=1
            if int(plo.co.plo.ploNo) == 2:
                plodata[1] += plo.marks
                plodataC[1]+=1
            if int(plo.co.plo.ploNo) == 3:
                plodata[2] += plo.marks
                plodataC[2]+=1
            if int(plo.co.plo.ploNo) == 4:
                plodata[3] += plo.marks
                plodataC[3]+=1
            if int(plo.co.plo.ploNo) == 5:
                plodata[4] += plo.marks
                plodataC[4]+=1
            if int(plo.co.plo.ploNo) == 6:
                plodata[5] += plo.marks
                plodataC[5]+=1
            if int(plo.co.plo.ploNo) == 7:
                plodata[6] += plo.marks
                plodataC[6]+=1
            if int(plo.co.plo.ploNo) == 8:
                plodata[7] += plo.marks
                plodataC[7]+=1
            if int(plo.co.plo.ploNo) == 9:
                plodata[8] += plo.marks
                plodataC[8]+=1
            if int(plo.co.plo.ploNo) == 10:
                plodata[9] += plo.marks
                plodataC[9]+=1
            if int(plo.co.plo.ploNo) == 11:
                plodata[10] += plo.marks
                plodataC[10]+=1
            if int(plo.co.plo.ploNo) == 12:
                plodata[11] += plo.marks
                plodataC[11]+=1
    for itr in range(0, 12, 1):
        try:
            plodata[itr] = plodata[itr]/plodataC[itr]
        except:
            plodata[itr] = plodata[itr]/1
        print(plodata[itr])
    return plodata
# FUNCTION OF GETTING DEPARTMENT-WISE PLO
def getDeptWisePLO(dept):
    plodata = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    plodataC = [0,0,0,0,0,0,0,0,0,0,0,0]
    plos = Assessment_T.objects.all()
    for plo in plos:
        if plo.studentID.department.departmentID == dept:
            if int(plo.co.plo.ploNo) == 1:
                plodata[0] += plo.marks
                plodataC[0]+=1
            if int(plo.co.plo.ploNo) == 2:
                plodata[1] += plo.marks
                plodataC[1]+=1
            if int(plo.co.plo.ploNo) == 3:
                plodata[2] += plo.marks
                plodataC[2]+=1
            if int(plo.co.plo.ploNo) == 4:
                plodata[3] += plo.marks
                plodataC[3]+=1
            if int(plo.co.plo.ploNo) == 5:
                plodata[4] += plo.marks
                plodataC[4]+=1
            if int(plo.co.plo.ploNo) == 6:
                plodata[5] += plo.marks
                plodataC[5]+=1
            if int(plo.co.plo.ploNo) == 7:
                plodata[6] += plo.marks
                plodataC[6]+=1
            if int(plo.co.plo.ploNo) == 8:
                plodata[7] += plo.marks
                plodataC[7]+=1
            if int(plo.co.plo.ploNo) == 9:
                plodata[8] += plo.marks
                plodataC[8]+=1
            if int(plo.co.plo.ploNo) == 10:
                plodata[9] += plo.marks
                plodataC[9]+=1
            if int(plo.co.plo.ploNo) == 11:
                plodata[10] += plo.marks
                plodataC[10]+=1
            if int(plo.co.plo.ploNo) == 12:
                plodata[11] += plo.marks
                plodataC[11]+=1
    for itr in range(0, 12, 1):
        try:
            plodata[itr] = plodata[itr]/plodataC[itr]
        except:
            plodata[itr] = plodata[itr]/1
    return plodata
# FUNCTION STUDENT-COURSE-WISE CO
def studentAndCourseWiseCO(student, courseT):
    cos = Assessment_T.objects.filter(studentID=student)
    codata = [0.00, 0.00, 0.00, 0.00]
    for co in cos:
        if co.co.course.courseID.lower() == courseT.lower():
            print(co.marks)
            if co.co.coNo == 1:
                codata[0] = co.marks
            if co.co.coNo == 2:
                codata[1] = co.marks
            if co.co.coNo == 3:
                codata[2] = co.marks
            if co.co.coNo == 4:
                codata[3] = co.marks
    return codata
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

            
            if request.method == 'POST':
                co = studentAndCourseWiseCO(request.user, request.POST['searchCourse'])
                return render(request, 'home/home.html', {  'cgpa': round(cgpa, 2),
                                                        'earned_credit': attempted_credit,
                                                        'plo': getPLO(request.user),
                                                        'co': co})
            return render(request, 'home/home.html', {  'cgpa': round(cgpa, 2),
                                                        'earned_credit': attempted_credit,
                                                        'plo': getPLO(request.user),
                                                        })
        # IF THE USER IS FACULTY
        if request.user.role == 'Faculty':
            ploS = None
            if request.method == 'POST':
                try:
                    student = User_T.objects.get(username=request.POST['searchStudent'])
                    ploS = getPLO(student)
                except:
                    pass
            return render(request, 'home/home.html', {  'plo': getDeptWisePLO(request.user.department.departmentID),
                                                        'ploStudent': ploS})
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

# Generate OBE Report Format CSV FOR Faculty
def generate_obe_format(request):
    if request.user.is_authenticated:
        if request.user.role == 'Faculty':
            if request.method == 'POST':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename=report_dated_{datetime.date.today()}.csv'
                
                # Create CSV Writer
                writer = csv.writer(response)
                # Write Heading Row
                writer.writerow(['STUDENT_ID',
                        'YEAR',
                        'SEMESTER',   
                        'COURSE',
                        'SECTION',
                        'CO1',
                        'CO2',
                        'CO3',
                        'CO4',
                        'GRADE',
                        ])
                if request.method == 'POST':
                    students = Enrollment_T.objects.filter(year=request.POST['year'])
                    for student in students:
                        if student.section.semester == request.POST['semester'] and student.section.faculty.username == request.user.username:
                            # Write the Data on each rows
                            writer.writerow([
                                student.student.username,
                                student.section.year,
                                student.section.semester,
                                student.section.course,
                                student.section.sectionNo,
                                '',
                                '',
                                '',
                                '',
                                '',
                                ])
                        
                return response
            return render(request, 'faculty/getOBEFormat.html', {})
        else:
            return redirect('home')
    else:
        return redirect('login')
# Generate OBE Report of Course in CSV FOR Faculty
def generate_obe_csv(request):
    if request.user.is_authenticated:
        if request.user.role == 'Faculty':
            if request.method == 'POST':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename=OBE_{datetime.date.today()}.csv'
                
                # Create CSV Writer
                
                # Write Heading Row
                print(request.user.is_superuser)
                header = ['STUDENT_ID',
                        'YEAR',
                        'SEMESTER',   
                        'COURSE',
                        'SECTION',
                        'CO1',
                        'CO2',
                        'CO3',
                        'CO4',
                        ]
                writer = csv.DictWriter(response, fieldnames = header)
                writer.writeheader()
                students = Assessment_T.objects.filter(year=request.POST['year'])
                for student in students:
                    if student.section.semester == request.POST['semester'] and student.section.faculty.username == request.user.username and student.section.course.courseID == request.POST['course']:
                        # Write the Data on each rows
                        # writer.writerow([
                        #     student.studentID.username,
                        #     student.section.year,
                        #     student.section.semester,
                        #     student.section.course,
                        #     student.section.sectionNo,
                        #     student.marks,
                        #     "",
                        #     None,
                        #     None,
                        # ])
                        if student.co.coNo == 1:
                            writer.writerow({
                                'STUDENT_ID': student.studentID.username,
                                'YEAR': student.section.year,
                                'SEMESTER': student.section.semester,
                                'COURSE': student.section.course,
                                'SECTION': student.section.sectionNo,
                                'CO1': student.marks,
                            })
                        if student.co.coNo == 2:
                            writer.writerow({
                                'STUDENT_ID': student.studentID.username,
                                'YEAR': student.section.year,
                                'SEMESTER': student.section.semester,
                                'COURSE': student.section.course,
                                'SECTION': student.section.sectionNo,
                                'CO2': student.marks,
                            })
                        if student.co.coNo == 3:
                            writer.writerow({
                                'STUDENT_ID': student.studentID.username,
                                'YEAR': student.section.year,
                                'SEMESTER': student.section.semester,
                                'COURSE': student.section.course,
                                'SECTION': student.section.sectionNo,
                                'CO3': student.marks,
                            })
                        if student.co.coNo == 4:
                            writer.writerow({
                                'STUDENT_ID': student.studentID.username,
                                'YEAR': student.section.year,
                                'SEMESTER': student.section.semester,
                                'COURSE': student.section.course,
                                'SECTION': student.section.sectionNo,
                                'CO4': student.marks,
                            })
                return response
            return render(request, 'faculty/getOBECourse.html', {'courses': Section_T.objects.filter(faculty=request.user)})
        else:
            return redirect('home')
    else:
        return redirect('login')