from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    # Faculty Path
    path('grade-input/', gradeInputForm, name='grade-input'),
    path('grade-input-csv/', gradeInputFromCSV, name='grade-input-csv'),
    path('generate-obe-format/', generate_obe_format, name='generate-obe-format'),
    path('generate-obe-csv/', generate_obe_csv, name='generate-obe-csv'),
    # Student Download Transcript
    path('transcript/', genTranscript, name='transcript'),
]
