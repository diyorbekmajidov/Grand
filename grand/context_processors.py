from .models import Student
from django.core.cache import cache
from django.shortcuts import redirect

def header_context(request):
    student_hemis_id = cache.get('student_hemis_id')
    if not cache.get('student_hemis_id'):
        return redirect('/auth/')
    student = Student.objects.get(student_id_number=student_hemis_id)

    return {'student_header':student}