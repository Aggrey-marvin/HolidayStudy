from django.contrib import admin
from .models import CurrentClass, TeacherSubject, Subject, Teacher, Student,TeacherEnrolmentSubject, TeacherEnrolment, StudentSubject, Testimonial

# Register your models here.
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(CurrentClass)
admin.site.register(TeacherEnrolment)
admin.site.register(TeacherEnrolmentSubject)
admin.site.register(TeacherSubject)
admin.site.register(StudentSubject)
admin.site.register(Testimonial)