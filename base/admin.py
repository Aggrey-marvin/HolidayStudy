from django.contrib import admin
from .models import CurrentClass, Subject, Teacher, Student, TeacherEnrolment

# Register your models here.
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(CurrentClass)
admin.site.register(TeacherEnrolment)