from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# School Database Table
class School_T(models.Model):
    schoolID = models.CharField(max_length=10, primary_key=True,null=False, blank=False)
    schoolName = models.CharField(max_length=255,null=False, blank=False)
    def __str__(self):
        return str(self.schoolID)
# Department Database Table
class Department_T(models.Model):
    departmentID = models.CharField(max_length=10, primary_key=True,null=False, blank=False)
    departmentName = models.CharField(max_length=255, null=False, blank=False)
    schoolID = models.ForeignKey(School_T, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.departmentID)
# Program Database Table
class Program_T(models.Model):
    programID = models.CharField(max_length=5, primary_key=True, null=False, blank=False)
    programName = models.CharField(max_length=255, null=False, blank=False)
    departmentID = models.ForeignKey(Department_T, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.programName)
# Course Table
class Course_T(models.Model):
    courseID = models.CharField(max_length=10, primary_key=True, null=False, blank=False)
    courseName = models.CharField(max_length=255, null=False, blank=False)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    creditNo = models.IntegerField()
    prerequisiteCourse = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.courseID)
# Custom User Table
class User_T(AbstractUser):
    ROLES_CHOICES=(
        ('Admin', 'Admin'),
        ('Faculty', 'Faculty'),
        ('Student', 'Student'),
    )
    username = models.CharField(max_length=255, primary_key=True)
    role = models.CharField(max_length=30, choices=ROLES_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE, null=True, blank=True)
# Section Table
class Section_T(models.Model):
    SEMESTER_CHOICES=(
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
    )
    sectionID = models.CharField(max_length=255, primary_key=True, null=False, blank=False)
    sectionNo = models.IntegerField(default=1)
    semester = models.CharField(max_length=30, choices=SEMESTER_CHOICES)
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE, default='N/A')
    faculty = models.ForeignKey(User_T, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.course)+ ' '+str(self.sectionNo)+ ' ' +str(self.semester)
# Enrollment Table
class Enrollment_T(models.Model):
    SEMESTER_CHOICES=(
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
    )
    enrollmentID = models.AutoField(primary_key=True)
    student = models.ForeignKey(User_T, on_delete=models.CASCADE)
    section = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    semester = models.CharField(max_length=30, choices=SEMESTER_CHOICES)
    year = models.CharField(max_length=4)

    def __str__(self):
        return str(self.enrollmentID)
# Program Learning Outcome Table
class PLO_T(models.Model):
    ploID = models.AutoField(primary_key=True)
    ploNo = models.IntegerField()
    details = models.CharField(max_length=255)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.ploNo)+ ' ' +str(self.program)
# Course Outcome Table
class CO_T(models.Model):
    coID = models.AutoField(primary_key=True)
    coNo = models.IntegerField(default=0)
    plo = models.ForeignKey(PLO_T, on_delete=models.CASCADE)
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.coNo)+ ' ' +str(self.plo)+ ' ' +str(self.course)
# Assessment Table
class Assessment_T(models.Model):
    assessmentNo = models.AutoField(primary_key=True)
    marks = models.FloatField()
    co = models.ForeignKey(CO_T, on_delete=models.CASCADE)
    section = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.assessmentNo)
# Evaluation Table
class Evaluation_T(models.Model):
    evaluationNo = models.AutoField(primary_key=True)
    obtainedMarks = models.FloatField()
    assessment = models.ForeignKey(Assessment_T, on_delete=models.CASCADE)
    enrollment = models.ForeignKey(Enrollment_T, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.evaluationNo)+' '+str(self.assessment)+' '+str(self.enrollment)
# Course GPA
class CourseGrade_T(models.Model):
    studentID = models.ForeignKey(User_T, on_delete = models.CASCADE)
    eduYear = models.CharField(max_length=4)
    eduSemester = models.CharField(max_length=25)
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE)
    section = models.IntegerField(default=1)
    grade = models.CharField(max_length=4)

    def __str__(self):
        return str(self.studentID)+' '+str(self.course)+' '+str(self.grade)