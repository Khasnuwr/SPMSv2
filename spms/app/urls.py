from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    path('plo-table/', studentWisePlo, name='plo'),
    path('co-course/', studentCourseWiseCO, name='co-course'),

    path('co-input/', gradeInputForm, name='co-input'),
    path('grade-input-csv/', gradeInputFromCSV, name='grade-input-csv'),
]
