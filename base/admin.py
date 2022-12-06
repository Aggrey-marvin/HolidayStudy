from django.contrib import admin
from .models import CurrentClass, TeacherSubject, Subject, Teacher, Student, TeacherEnrolment, Testimonial

# Register your models here.
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(CurrentClass)
admin.site.register(TeacherEnrolment)
admin.site.register(TeacherSubject)
admin.site.register(Testimonial)