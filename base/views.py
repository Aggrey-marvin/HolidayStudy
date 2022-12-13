from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from . models import Teacher, Student, Subject, StudentSubject, TeacherEnrolment, TeacherSubject, Testimonial

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
  navbar = 'index'
  teachers = Teacher.objects.all()
  subjects = Subject.objects.all()
  testimonials = Testimonial.objects.all()
  
  context = {
    'navbar': navbar,
    'teachers': teachers,
    'subjects': subjects,
    'testimonials': testimonials,
  }
  return render(request, 'base/home.html', context)

def aboutUs(request):
  navbar = 'about'
  
  context = {
    'navbar': navbar,
  }
  return render(request, 'base/about.html', context)

class TestimonialCreateView(CreateView):
  model = Testimonial
  fields = ['message']
  template_name = 'base/testimonial_create.html'
  
  def form_valid(self, form):
    teacher = Teacher.objects.filter(teacherName=self.request.user.id)
    student = Student.objects.filter(studentName=self.request.user.id)

    if teacher:
      role = 'teacher'
    elif student:
      role = 'student'
    else:
      role = 'user'

    form.instance.author = self.request.user
    form.instance.role = role
    return super().form_valid(form)
  
  success_url = reverse_lazy('base:index')

# Student views are below here
def studentPage(request):
  navbar = 'students'
  # Check whether student is registered
  isRegistered = Student.objects.filter(studentName=request.user.id)
  
  isTeacher = Teacher.objects.filter(teacherName=request.user.id)
  if isTeacher:
    return redirect('base:notStudent')
  else:
    students = Student.objects.all()
    
    context = {
      'students': students,
      'isRegistered': isRegistered,
      'navbar': navbar,
    }
    return render(request, 'base/student_page.html', context)

class StudentCreateView(CreateView):
  model = Student
  fields = ['currentSchool', 'subjects', 'currentClass', 'studentImage']
  template_name = 'base/create_student.html'
  
  def form_valid(self, form):
    form.instance.studentName = self.request.user
    return super().form_valid(form)
  
  success_url = reverse_lazy('base:studentPage')
  
def viewSubjectTeachers(request, id):
  subject = Subject.objects.get(pk=id)
  teachers = TeacherSubject.objects.filter(subject=id)
  
  context = {
    'teachers': teachers,
    'subject': subject
  }
  return render(request, 'base/view_subject_teachers.html', context)

def viewSubjects(request):
  navbar = 'subjects'
  subjects = Subject.objects.all()
  
  context = {
    'subjects': subjects,
    'navbar': navbar,
  }
  return render(request, 'base/subjects_page.html', context)

# Teacher views are from this point onwards
def teacherPage(request):
  navbar = "viewTeacher"
  isRegistered = Teacher.objects.filter(teacherName=request.user.id)
  isStudent = Student.objects.filter(studentName=request.user.id)

  # The code belo was supposed to restrict a student from accessing the teacher page
  # if isStudent:
  #   return redirect('base:notTeacher')
  
  teachers = Teacher.objects.all()
  
  context = {
    'teachers': teachers,
    'isRegistered': isRegistered,
    'isStudent': isStudent,
    'navbar': navbar,
  }
  return render(request, 'base/teacher_page.html', context)

class TeacherCreateView(CreateView):
  model = Teacher
  fields = ['subjects', 'currentSchool', 'teacherFee', 'teacherImage']
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
  navbar = 'viewTeacher'
  teachers = Teacher.objects.all()
  
  context = {
    'teachers': teachers,
    'navbar': navbar,
  }
  return render(request, 'base/view_teachers.html', context)

@login_required(login_url='base:login')
def enrol(request): 
  # Getting logged teacher
  teacherId = request.GET['teacherId']
  
  # Getting the student enroling
  currentUser = request.user
  student = Student.objects.filter(studentName=currentUser.id)
  
  # Checking whether current user is actually a student.
  if student:
    teacher = Teacher.objects.get(id=teacherId)
    studentSubjects = StudentSubject.objects.all()
    teacherSubjects = TeacherSubject.objects.all()
    
    # Varible to confirm whether a teacher teaches a particular subject
    teaches = False
    
    for studentSubject in studentSubjects:
      for teacherSubject in teacherSubjects:
        if studentSubject.subject is teacherSubject.subject:
          teaches = True
          break
      else:
        continue
      break
      
    if teaches:
      if request.method == 'POST':
        teacherId = request.POST['teacherId']
        student = Student.objects.get(studentName=currentUser.id)
        enrolment = TeacherEnrolment(teacher=teacher, student=student)
        enrolment.save()
        return redirect('base:viewTeacher')
      else:
        return redirect('base:wrongTeacher')
  else:
    return redirect('base:unauthorised')
  
  teacher = Teacher.objects.get(id=teacherId)

  context = {
    'teacher': teacher,
    'student': student,
  }
  
  return render(request, 'base/confirm_enrolment.html', context)

def wrongTeacher(request):
  
  return render(request, 'base/wrong_teacher.html')

def notStudent(request):
  
  return render(request, 'base/not_student.html')

def notTeacher(request):
  
  return render(request, 'base/not_teacher.html')