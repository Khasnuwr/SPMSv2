from django.db import models

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
    departmentName = models.CharField(max_length=255, ,null=False, blank=False)
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
    pass