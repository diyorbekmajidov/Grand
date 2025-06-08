from django.db import models


class Student(models.Model):
    student_name = models.CharField(max_length=56, blank=True, null=True)
    phone_number = models.CharField(max_length=56, blank=True, null=True)
    student_imeg = models.ImageField(upload_to='media/')
    student_id_number = models.CharField(max_length=16, unique=True, blank=True, null=True)
    email = models.CharField(max_length=86)
    passport_number = models.CharField(max_length=12)
    birth_date = models.CharField(max_length=50)
    groups = models.JSONField()
    studentStatus = models.CharField(max_length=86)
    paymentForm = models.CharField(max_length=86)
    faculty = models.CharField(max_length=86)
    level = models.CharField(max_length=86)
    avg_gpa = models.CharField(max_length=86)

    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_name
