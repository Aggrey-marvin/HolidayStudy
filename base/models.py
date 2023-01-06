# import jsonfield
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
  subjectName = models.CharField(max_length=256)
  subjectImage = models.ImageField(upload_to="photos/%y/%m/%d", blank=True)
  
  def __str__(self):
    return self.subjectName
  
class CurrentClass(models.Model):
  className = models.CharField(max_length=256)
  
  def __str__(self):
    return self.className
  
class Student(models.Model):
  studentName = models.ForeignKey(User, on_delete=models.CASCADE)
  currentSchool = models.CharField(max_length=500)
  subjects = models.ManyToManyField(Subject, through='StudentSubject')
  currentClass = models.ForeignKey(CurrentClass, on_delete=models.CASCADE)
  studentImage = models.ImageField(upload_to="photos/%y/%m/%d", blank=True)
  
  def __str__(self):
    return self.studentName.last_name
  
class Teacher(models.Model):
  teacherName = models.ForeignKey(User, on_delete=models.CASCADE)
  subjects = models.ManyToManyField(Subject, through='TeacherSubject')
  students = models.ManyToManyField(Student, through='TeacherEnrolment')
  currentSchool = models.CharField(max_length=400)
  teacherImage = models.ImageField(upload_to="photos/%y/%m/%d", blank=True)
  teacherDescription = models.TextField()
  teacherFee = models.IntegerField()
  
  def __str__(self):
    return self.teacherName.last_name
  
class TeacherSubject(models.Model):
  teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
  subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
  
class StudentSubject(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
  
class TeacherEnrolment(models.Model):
  teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  subjects = models.ManyToManyField(Subject, through="TeacherEnrolmentSubject")
  
  class Meta:
    unique_together = [['teacher', 'student']]
    
class TeacherEnrolmentSubject(models.Model):
  teacherEnrolment = models.ForeignKey(TeacherEnrolment, on_delete=models.CASCADE)
  subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
class Testimonial(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  message = models.TextField()
  role = models.CharField(max_length=256)
  
  def __str__(self):
    return self.author.username