from django.db import models
from django.contrib.auth.models import User
from Parent.models import Parent_Reg
from SiteAdmin.models import Subject
from Teacher.models import Homework,Teacher_Reg


# Create your models here.
class Student_Reg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent_Reg, on_delete=models.CASCADE)
    class_level = models.CharField(max_length=20)
    admission_date = models.DateField(auto_now_add=True)
    gender=models.CharField(max_length=100,default='null')
    subjects = models.ManyToManyField(Subject) 
    status=models.CharField(max_length=100,default='pending')
    def __str__(self):
     return f"{self.user.first_name} {self.user.last_name}"

class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_file = models.FileField(upload_to='homework_submissions/') 
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,default='pending')

class StudentTeacherMessage(models.Model):
    student = models.ForeignKey(Student_Reg, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher_Reg, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)