from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Assigning Field list in 'fields' variable
fields = list(UserAdmin.fieldsets)
# Serializing these fields in the fields[1] index of list fields
fields[1] = ('Personal Info', { 'fields': ('first_name',  'last_name', 'email', 'phone', 'program', 'department', 'role')})
# Storing fields list as tuple in UserAdmin fieldsets
UserAdmin.fieldsets = tuple(fields)
# Registering User_T in the AdminPanel
admin.site.register(User_T, UserAdmin)
admin.site.register(Program_T)
admin.site.register(Department_T)
admin.site.register(Course_T)
admin.site.register(School_T)