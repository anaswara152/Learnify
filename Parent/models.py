from django.db import models
from django.contrib.auth.models import User
from SiteAdmin.models import Subject,Fee
from Teacher.models import Teacher_Reg

# Create your models here.
class Parent_Reg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    gender=models.CharField(max_length=100,default='null')
    status=models.CharField(max_length=100,default='pending')
    

class Mark_marks(models.Model):
    student = models.ForeignKey('Student.Student_Reg',on_delete=models.CASCADE,related_name='marks')
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='marks')
    teacher = models.ForeignKey(Teacher_Reg,on_delete=models.SET_NULL,null=True,blank=True,related_name='given_marks')
    parent = models.ForeignKey(Parent_Reg,on_delete=models.SET_NULL,null=True,blank=True,related_name='added_marks')
    class_level = models.CharField(max_length=20)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()
    date = models.DateField(auto_now_add=True)

class ParentTeacherMessage(models.Model):
    parent = models.ForeignKey('Parent.Parent_Reg', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher.Teacher_Reg', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Payment(models.Model):
    parent = models.ForeignKey(Parent_Reg, on_delete=models.CASCADE)
    student = models.ForeignKey('Student.Student_Reg', on_delete=models.CASCADE)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)

    amount_paid = models.FloatField()
    card_holder_name = models.CharField(max_length=100,blank=True,null=True)
    card_number = models.CharField(max_length=16)

    payment_date = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message