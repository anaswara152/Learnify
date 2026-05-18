from django.db import models
from django.contrib.auth.models import User
from SiteAdmin.models import Subject

# Create your models here.
class Teacher_Reg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender=models.CharField(max_length=100,default='null')
    qualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    phone=models.CharField(max_length=10,default='null')
    subjects = models.ManyToManyField(Subject) 
    profile_picture = models.ImageField(upload_to='teacher_profiles/',null=True,blank=True)
    certificates=models.FileField(upload_to='certificates/',null=True,blank=True)
    id_card=models.FileField(upload_to='proof',default='null')
    status=models.CharField(max_length=100,default='pending')

class LiveClass(models.Model):
    teacher = models.ForeignKey(Teacher_Reg, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_level = models.CharField(max_length=20,default='null')
    class_date = models.DateField()
    class_time = models.TimeField()
    meeting_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)


class RecordedClass(models.Model):
    teacher = models.ForeignKey(Teacher_Reg, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_level = models.CharField(max_length=20,default='null')
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='recorded_classes')
    uploaded_at = models.DateTimeField(auto_now_add=True)    

class Notes(models.Model):
    teacher = models.ForeignKey(Teacher_Reg, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_level = models.CharField(max_length=20,default='null')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Homework(models.Model):
    teacher = models.ForeignKey(Teacher_Reg, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_level = models.CharField(max_length=20,default='null')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='homework/')
    due_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_attendance')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True,blank=True)
    class_level = models.CharField(max_length=20,default='null')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_attendance')
    date = models.DateField()
    status = models.CharField(max_length=10,default='pending')


