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
# Section Table
class Section_T(models.Model):
    pass
# Custom User Table
class User_T(AbstractUser):
    ROLES_CHOICES=(
        ('Admin', 'Admin'),
        ('Faculty', 'Faculty'),
        ('Student', 'Student'),
    )
    role = models.CharField(max_length=30, choices=ROLES_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE, null=True, blank=True)