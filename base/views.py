from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from . models import Teacher, Student, TeacherEnrolment

# Create your views here.

def registerUser(request):
  form = SignUpForm()
  
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('base:index')
    else:
      messages.error(request, "Form Error:(")
      return redirect('base:register')
  
  context = {
    'form': form
  }
  return render(request, "base/create_user.html", context)

def userCreated(request):
  
  return render(request, "base/user_created_success.html")

def unauthorisedUser(request):
  
  return render(request, 'base/unauthorised_user.html')
  
def loginUser(request):
  
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
      login(request, user)
      return redirect('base:index')
    else:
      messages.error("The login details do not match.")
      return redirect('base:login')
    
  return render(request, 'base/login_user.html')
  
   
def logoutUser(request):
  logout(request)
  
  return redirect('base:index')

def index(request):
  
  return render(request, 'base/home.html')

# Student views are below here
def studentPage(request):
  isTeacher = Teacher.objects.filter(teacherName=request.user.id)
  if isTeacher:
    return redirect('base:notStudent')
  else:
    students = Student.objects.all()
    
    context = {
      'students': students
    }
    return render(request, 'base/student_page.html', context)

class StudentCreateView(CreateView):
  model = Student
  fields = ['currentSchool', 'subjects', 'currentClass']
  template_name = 'base/create_student.html'
  
  def form_valid(self, form):
    form.instance.studentName = self.request.user
    return super().form_valid(form)
  
  success_url = reverse_lazy('base:studentPage')

# Teacher views are from this point onwards
def teacherPage(request):
  teachers = Teacher.objects.all()
  
  context = {
    'teachers': teachers
  }
  return render(request, 'base/teacher_page.html', context)

class TeacherCreateView(CreateView):
  model = Teacher
  fields = ['subjects', 'currentSchool']
  template_name = 'base/create_teacher.html'
  
  def form_valid(self, form):
    form.instance.teacherName = self.request.user
    return super().form_valid(form)
    
  
  success_url = reverse_lazy('base:teacherPage')
  
class TeacherDetailView(DetailView):
  model = Teacher
  context_object_name = 'teacher'
  template_name = 'base/teacher_detail.html'
  
def teacherProfile(request, pk):
  teacher = Teacher.objects.get(pk=pk)
  students = TeacherEnrolment.objects.filter(teacher=teacher.id)
  
  context = {
    'teacher': teacher, 
    'students': students,
  }
  return render(request, 'base/teacher_profile.html', context)
  
def viewTeacher(request):
  teachers = Teacher.objects.all()
  
  context = {
    'teachers': teachers,
  }
  return render(request, 'base/view_teachers.html', context)

@login_required(login_url='base:login')
def enrol(request): 
  teacherId = request.GET['teacherId']
  currentUser = request.user
  student = Student.objects.filter(studentName=currentUser.id)
  
  if student:
    if request.method == 'POST':
      teacherId = request.POST['teacherId']
      teacher = Teacher.objects.get(id=teacherId)
      enrolment = TeacherEnrolment(teacher=teacher, student=student)
      enrolment.save()
      return redirect('base:viewTeacher')
  else:
    return redirect('base:unauthorised')
  
  teacher = Teacher.objects.get(id=teacherId)

  context = {
    'teacher': teacher,
    'student': student,
  }
  
  return render(request, 'base/confirm_enrolment.html', context)

def notStudent(request):
  
  return render(request, 'base/not_student.html')