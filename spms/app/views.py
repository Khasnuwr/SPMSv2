from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *
from django.db import connection
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
    # studentT = User_T.objects.get(username=student)
    student = User_T.objects.raw("SELECT id FROM app_user_t WHERE username=%s;", [student])[0]
    if student.role != 'Student':
        return None
    print(student.username)
    # filtering the PLOs where the assessment_t has the studentid we needed
    plos = Assessment_T.objects.raw('SELECT * FROM app_assessment_t WHERE studentID_id = %s;', [student.id])
    plodata = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    for plo in plos:
        print(f'PLO{plo.co.plo.ploNo} CO{plo.co.coNo} {plo.marks} {plo.studentID}')
        #if plo.studentID.username == studentT.username:
        print(plo.studentID.username, student.username)
        # print(f'PLO{plo.co.plo.ploNo} CO{plo.co.coNo} {plo.marks} {plo.studentID}')
        if int(plo.co.plo.ploNo) == 1:
            plodata[0] += plo.marks
        if int(plo.co.plo.ploNo) == 2:
            plodata[1] += plo.marks
        if int(plo.co.plo.ploNo) == 3:
            plodata[2] += plo.marks
        if int(plo.co.plo.ploNo) == 4:
            plodata[3] += plo.marks
        if int(plo.co.plo.ploNo) == 5:
            plodata[4] += plo.marks
        if int(plo.co.plo.ploNo) == 6:
            plodata[5] += plo.marks
        if int(plo.co.plo.ploNo) == 7:
            plodata[6] += plo.marks
        if int(plo.co.plo.ploNo) == 8:
            plodata[7] += plo.marks
        if int(plo.co.plo.ploNo) == 9:
            plodata[8] += plo.marks
        if int(plo.co.plo.ploNo) == 10:
            plodata[9] += plo.marks
        if int(plo.co.plo.ploNo) == 11:
            plodata[10] += plo.marks
        if int(plo.co.plo.ploNo) == 12:
            plodata[11] += plo.marks
    return plodata
# FUNCTION OF GETTING DEPARTMENT-WISE PLO
def getDeptWisePLO(dept):
    plodata = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    plodataC = [0,0,0,0,0,0,0,0,0,0,0,0]
    # Get all the assessments from the assessment_t
    plos = Assessment_T.objects.raw('SELECT * FROM app_assessment_t;')

    for plo in plos:
        # Filter all the Assessments from the assessment_t by Department
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
    # Filter all the Assessments from Assessment_T table by student_id
    cos = Assessment_T.objects.raw("SELECT * FROM app_assessment_t WHERE studentID_id = %s ;", [student.id])
    codata = [0.00, 0.00, 0.00, 0.00]
    for co in cos:
        # Filter all the Filtered assignments by the course_id by chaining Assignment chaining CO chaining course_id
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
            # Get all the grades from CourseGrade_T filtered by a specific student_id
            grades = CourseGrade_T.objects.raw("SELECT * FROM app_coursegrade_t WHERE studentID_id = %s;", [request.user.id])
            attempted_credit = 0
            total_cum_credit = 0

            for grade in grades:
                if grade.grade == 'A':
                    #course = Course_T.objects.get(pk=grade.course)
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*4.00)
                elif grade.grade == 'A-':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.70)
                elif grade.grade == 'B+':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.30)
                elif grade.grade == 'B':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.00)
                elif grade.grade == 'B-':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.70)
                elif grade.grade == 'C+':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.30)
                elif grade.grade == 'C':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.00)
                elif grade.grade == 'C-':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.70)
                elif grade.grade == 'D+':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.30)
                elif grade.grade == 'D':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.00)
                elif grade.grade == 'F':
                    #course = Course_T.objects.get(pk=grade.course)
                    #attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*0.00)
            try:
                cgpa = total_cum_credit/attempted_credit
            except:
                cgpa = 0.0
            if request.method == 'POST':
                co = studentAndCourseWiseCO(request.user, request.POST['searchCourse'])
                return render(request, 'home/home.html', {  'cgpa': round(cgpa, 2),
                                                        'earned_credit': attempted_credit,
                                                        'plo': getPLO(request.user.username),
                                                        'co': co})
            return render(request, 'home/home.html', {  'cgpa': round(cgpa, 2),
                                                        'earned_credit': attempted_credit,
                                                        'plo': getPLO(request.user.username),
                                                        })
        # IF THE USER IS FACULTY
        if request.user.role == 'Faculty':
            ploS = None
            if request.method == 'POST':
                try:
                    ploS = getPLO(request.POST['searchStudent'])
                except:
                    pass
            return render(request, 'home/home.html', {  'plo': getDeptWisePLO(request.user.department.departmentID),
                                                        'ploStudent': ploS})
        
        if request.user.role == 'Admin':
            departments=Department_T.objects.raw("SELECT * FROM app_department_t;")
            if request.method == 'POST':
                return render(request, 'home/home.html', {  'ploDepartment': getDeptWisePLO(request.POST['department']),
                                                            'departments': departments})
            return render(request, 'home/home.html', { 'departments': departments})
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
            student = User_T.objects.raw("SELECT * FROM app_user_t WHERE username=%s;", [request.user.username])[0]
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
            # Get All the Course's grades filtered by student id
            grades = CourseGrade_T.objects.raw("SELECT * FROM app_coursegrade_t WHERE studentID_id = %s;", [request.user.id])
            attempted_credit = 0
            total_cum_credit = 0

            for grade in grades:
                if grade.grade == 'A':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*4.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  4.00                    A                  {float(int(course.creditNo)*4.00)}")
                elif grade.grade == 'A-':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.70)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  3.70                    A-                  {round(float(int(course.creditNo)*3.70), 2)}")
                elif grade.grade == 'B+':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.30)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  3.30                    B+                  {round(float(int(course.creditNo)*3.30), 2)}")
                elif grade.grade == 'B':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*3.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  3.00                    B                  {float(int(course.creditNo)*3.00)}")
                elif grade.grade == 'B-':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.70)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  2.70                    B-                  {round(float(int(course.creditNo)*2.70), 2)}")
                elif grade.grade == 'C+':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.30)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  2.30                    C+                  {round(float(int(course.creditNo)*2.30), 2)}")
                elif grade.grade == 'C':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*2.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  2.00                    C                  {float(int(course.creditNo)*2.00)}")
                elif grade.grade == 'C-':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.70)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  1.70                    C-                  {round(float(int(course.creditNo)*1.70), 2)}")
                elif grade.grade == 'D+':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.30)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  1.30                    D+                  {round(float(int(course.creditNo)*1.30), 2)}")
                elif grade.grade == 'D':
                    course = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [grade.course.courseID])[0]
                    attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*1.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  1.00                    D                  {float(int(course.creditNo)*1.00)}")
                elif grade.grade == 'F':
                    #course = Course_T.objects.get(pk=grade.course)
                    #attempted_credit+=int(course.creditNo)
                    total_cum_credit+=float(int(course.creditNo)*0.00)

                    lines.append(f"{course.courseID}                        {grade.eduSemester}                       {grade.eduYear}                     {course.creditNo}                  0.00                    F                  {float(int(course.creditNo)*0.00)}")
            try:
                cgpa = total_cum_credit/attempted_credit
            except:
                cgpa = 0.0
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
                    # Filter the student from user_t table by Student_ID
                    student_ID = User_T.objects.raw("SELECT * FROM app_user_t WHERE username=%s;", [request.POST['studentID']])[0]
                    # Filter the Course from the course_t by Course_ID
                    courseT = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [request.POST['course']])[0]
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
from io import TextIOWrapper
def gradeInputFromCSV(request):
    if request.user.is_authenticated:
        if request.user.role == 'Faculty':
            success = 'success'
            if request.method == 'POST':
                csv_file = request.FILES['csv_file']
                #data_frame = pd.read_csv(csv_file, index_col=False, iterator=True)
                data_frame = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'))
                print(data_frame)
                try:
                    for row in data_frame:
                        print(row)
                        try:
                            # Get the student object filtering Student_ID importing from CSV data_frame
                            student = User_T.objects.raw("SELECT * FROM app_user_t WHERE username=%s;", [str(row[0])])[0]
                            # Getting Course Object filtering course_ID importing from CSV data_frame
                            courseT = Course_T.objects.raw("SELECT * FROM app_course_t WHERE courseID = %s;", [str(row[3])])[0] 
                            print('touches')
                            data = CourseGrade_T(studentID=student,
                                eduYear=str(row[1]),
                                eduSemester=str(row[2]),
                                course=courseT,
                                section=str(row[4]),
                                grade=str(row[9])
                            )
                            data.save()
                            cos = CO_T.objects.filter(course=courseT)
                            for cot in cos:
                                if cot.coNo == 1 and str(row[5]) != '':
                                    form = Assessment_T(
                                        studentID=student,
                                        semester=str(row[2]),
                                        year=str(row[1]),
                                        marks=str(row[5]),
                                        co=cot,
                                        # Filtering section by section number AND course_id
                                        section=Section_T.objects.raw("SELECT * FROM app_section_t WHERE sectionNo=%s AND course_id=%s LIMIT 1;", [str(row[4]), courseT.courseID])[0]
                                        
                                    )
                                    form.save()
                                if cot.coNo == 2 and str(row[6]) != '':
                                    form = Assessment_T(
                                        studentID=student,
                                        semester=str(row[2]),
                                        year=str(row[1]),
                                        marks=str(row[6]),
                                        co=cot,
                                        # Filtering section by section number AND course_id
                                        section=Section_T.objects.raw("SELECT * FROM app_section_t WHERE sectionNo=%s AND course_id=%s LIMIT 1;", [str(row[4]), courseT.courseID])[0]
                                    )
                                    form.save()
                                if cot.coNo == 3 and str(row[7]) != '':
                                    form = Assessment_T(
                                        studentID=student,
                                        semester=str(row[2]),
                                        year=str(row[1]),
                                        marks=str(row[7]),
                                        co=cot,
                                        # Filtering section by section number AND course_id
                                        section=Section_T.objects.raw("SELECT * FROM app_section_t WHERE sectionNo=%s AND course_id=%s LIMIT 1;", [str(row[4]), courseT.courseID])[0]
                                    )
                                    form.save()
                                if cot.coNo == 4 and str(row[8]) != '':
                                    form = Assessment_T(
                                        studentID=student,
                                        semester=str(row[2]),
                                        year=str(row[1]),
                                        marks=str(row[8]),
                                        co=cot,
                                        # Filtering section by section number AND course_id
                                        section=Section_T.objects.raw("SELECT * FROM app_section_t WHERE sectionNo=%s AND course_id=%s LIMIT 1;", [str(row[4]), courseT.courseID])[0]
                                    )
                                    form.save()
                        except:
                            pass
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
                # Write Heading Row's columns
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
                    # Get all the Enrollments from Enrollment_T table filtered with the inserted year OR filtered with specific year and store it as student
                    students = Enrollment_T.objects.raw("SELECT * FROM app_enrollment_t WHERE year=%s;", [request.POST['year']])
                    for student in students:
                        # Filter the Enrollment's section's semester and section's appointed faculty 
                        if student.section.semester == request.POST['semester'] and student.section.faculty.username == request.user.username:
                            # Write the Data on each rows which has these corresponding columns -> student_id, year, semester, course, section_no, co1, co2, co3, co4
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
                co1 = None
                co2 = None
                co3 = None
                writer = csv.DictWriter(response, fieldnames = header)
                writer.writeheader()
                # Get all the assessments from assessment_t filtering by the inserted year by Faculty User
                students = Assessment_T.objects.raw("SELECT * FROM app_assessment_t WHERE year=%s;", [request.POST['year']])
                for student in students:
                    # Filtering assessments by the inserted semester and the Faculty User who is assigned to the section
                    if student.section.semester == request.POST['semester'] and student.section.faculty.username == request.user.username and student.section.course.courseID == request.POST['course']:
                        if student.co.coNo == 1:
                            co1 = student.marks
                        if student.co.coNo == 2:
                            co2 = student.marks
                        if student.co.coNo == 3:
                            co3 = student.marks
                        if student.co.coNo == 4:
                            co4 = student.marks
                            writer.writerow({
                                'STUDENT_ID': student.studentID.username,
                                'YEAR': student.section.year,
                                'SEMESTER': student.section.semester,
                                'COURSE': student.section.course,
                                'SECTION': student.section.sectionNo,
                                'CO1': co1,
                                'CO2': co2,
                                'CO3': co3,
                                'CO4': student.marks,
                            })
                del co1
                del co2
                del co3
                return response
                # Get all the courses with corresponding Sections which were assigned to the current logged in Faculty User 
            return render(request, 'faculty/getOBECourse.html', {'courses': Section_T.objects.raw("SELECT * FROM app_section_t WHERE faculty_id=%s;", [request.user.id]) })
        else:
            return redirect('home')
    else:
        return redirect('login')
# Admin Part
def admin_page(request):
    if request.user.is_authenticated:
        if request.user.role == 'Admin':
            return render(request, 'admin/notice_page.html', {})
        else:
            return redirect('home')
    else:
        return redirect('login')