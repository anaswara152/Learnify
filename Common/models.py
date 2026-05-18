from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ReviewRemark(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey('Student.Student_Reg', on_delete=models.CASCADE)
    review = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    review_status = models.CharField(max_length=20, default='pending')
    remark_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_by} -> {self.student}"
    

