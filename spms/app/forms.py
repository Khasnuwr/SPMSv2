from .models import *
from django import forms
from django.forms import ModelForm

class GradeInputForm(ModelForm):
    class Meta:
        model = CourseGrade_T
        fields = '__all__'