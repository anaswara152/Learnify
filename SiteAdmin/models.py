from django.db import models

# Create your models here.
class Subject(models.Model):
    subjectname=models.CharField(max_length=100)
    def __str__(self):
        return self.subjectname
    


class Fee(models.Model):
    student = models.ForeignKey(
        'Student.Student_Reg',
        on_delete=models.CASCADE,
        related_name='fees'
    )
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='subject_fees',null=True,blank=True
    )

    amount_due = models.FloatField()
    amount_paid = models.FloatField(default=0)
    due_date = models.DateField()

    status = models.CharField(max_length=20, default='unpaid')

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject}"

class TeacherSalary(models.Model):
    teacher = models.ForeignKey('Teacher.Teacher_Reg',on_delete=models.CASCADE,related_name='salaries')
    month = models.CharField(max_length=20)  
    amount = models.FloatField()
    status = models.CharField(max_length=20,default='unpaid')
    paid_date = models.DateField(auto_now=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=100,default='pending')
    account_holder_name = models.CharField(max_length=100,null=True,blank=True)
    account_number = models.CharField(max_length=20,null=True,blank=True)  
    transaction_id = models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        unique_together = ('teacher', 'month')



class TeacherAttendance(models.Model):
    teacher = models.ForeignKey('Teacher.Teacher_Reg',on_delete=models.CASCADE,related_name='teacher_attendance')
    date = models.DateField()
    status = models.CharField(max_length=10,default='notmarked')
    marked_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('teacher', 'date')