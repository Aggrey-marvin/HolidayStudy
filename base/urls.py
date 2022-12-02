from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path('registerUser/', views.registerUser, name='register'),
    path('userCreated/', views.userCreated, name="userCreated"),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.index, name="index"),
    path('unauthorised/', views.unauthorisedUser, name="unauthorised"),
    path('about/', views.aboutUs, name='about'),
    
    # Urls for student's views are below this
    path('studentPage', views.studentPage, name="studentPage"),
    path('postStudent', views.StudentCreateView.as_view(), name="postStudent"),
    path('viewTeachers', views.viewTeacher, name="viewTeacher"),
    path('confirmEnrolment', views.enrol, name="confirmEnrolment"),
    path('notStudent/', views.notStudent, name="notStudent"),
    path('subjects/', views.viewSubjects, name="subjects"),
    
    # Urls for teacher's views are below this
    path('teacherPage', views.teacherPage, name="teacherPage"),
    path('postTeacher/', views.TeacherCreateView.as_view(), name="postTeacher"),
    path('teacherDetail/<pk>', views.TeacherDetailView.as_view(), name="teacherDetail"),
    path('teacherProfile/<pk>', views.teacherProfile, name="teacherProfile"),
    path('notTeacher/', views.notTeacher, name="notTeacher"),
]

