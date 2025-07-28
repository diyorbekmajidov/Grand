from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError


def validate_img_size(value):
    file_size = value.size
    if file_size >5* 1024 * 1024:
        raise ValidationError("Yuklanishi mumkin bo'lgan maksimal fayl hajmi 1MB.")
    return value

class Student(models.Model):
    student_name = models.CharField(max_length=56, blank=True, null=True, verbose_name="Talaba_Ismi")
    phone_number = models.CharField(max_length=56, blank=True, null=True, verbose_name="Telfon-raqam")
    student_imeg = models.ImageField(upload_to='media/', verbose_name="rasm")
    student_id_number = models.CharField(max_length=16, unique=True, blank=True, null=True)
    email = models.CharField(max_length=86)
    passport_number = models.CharField(max_length=12, verbose_name="passport raqami")
    birth_date = models.CharField(max_length=50, verbose_name="Tug'ilgan-kun-sanasi")
    groups = models.JSONField()
    studentStatus = models.CharField(max_length=86, verbose_name="talaba-holati")
    paymentForm = models.CharField(max_length=86, verbose_name="to'lov shakli")
    faculty = models.CharField(max_length=86, verbose_name="fakultet")
    level = models.CharField(max_length=86, verbose_name="kurs")
    avg_gpa = models.CharField(max_length=86, verbose_name="Gpa-bali")

    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_name


class Criteria(models.Model):
    title = models.CharField(max_length=56)
    score = models.IntegerField(default=0)
    description = models.CharField(max_length=500, blank=True, null=True)

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
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to='student_uploads/')
    task_score = models.IntegerField(blank=True, null=True)
    initial_score = models.IntegerField(blank=True, null=True)
    is_scored = models.BooleanField(default=False, verbose_name="Baholandi")
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True)
    supervisor_comment = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'criteria')

    def save(self, *args, **kwargs):
        if self.pk:  # update holatida
            old = StudentFiles.objects.get(pk=self.pk)
            if old.is_scored:
                if self.task_score != old.task_score or self.initial_score != old.initial_score:
                    raise ValidationError("Baholangan faylga qayta baho qo‘yish mumkin emas.")
        else:
            if self.initial_score is None and self.criteria:
                self.initial_score = self.criteria.score
                self.task_score = self.criteria.score

        super().save(*args, **kwargs)

    def score_ratio_display(self):
        if self.is_scored and self.initial_score and self.task_score is not None:
            return f"{self.task_score}/{self.initial_score}"
        return "Baholanmagan"

    def __str__(self):
        return f"{self.student}-{self.criteria}"

