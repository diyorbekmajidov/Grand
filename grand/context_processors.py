from .models import Student
from django.core.cache import cache
from django.shortcuts import redirect

def header_context(request):
    student_hemis_id = cache.get('student_hemis_id')
    if not student_hemis_id:
        return {}  # Bo‘sh dict qaytaring, redirect bu yerda ishlamaydi
    try:
        student = Student.objects.get(student_id_number=student_hemis_id)
    except Student.DoesNotExist:
        return {}
    return {'student_header': student}
