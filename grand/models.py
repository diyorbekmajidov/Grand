from django.db import models
from django.contrib.auth.models import User

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


class Criteria(models.Model):
    title = models.CharField(max_length=56, blank=True, null=True)
    score = models.IntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class StudentFiles(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)  # agar Student modeli bo‘lsa
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to='student_uploads/')
    task_score = models.IntegerField(blank=True, null=True)  # nazoratchi o‘zgartiradi
    initial_score = models.IntegerField(blank=True, null=True)  # criteria.score bu yerga saqlanadi
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True)
    supervisor_comment = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.initial_score is None and self.criteria:
            self.initial_score = self.criteria.score
            self.task_score = self.criteria.score  # birinchi yuklashda default beriladi
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student} - {self.criteria}'
