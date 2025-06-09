from django.contrib import admin
from .models import Student, Supervisor, StudentFiles, Criteria
import json

class StudentAdmin(admin.ModelAdmin):
    list_display = ('passport_number', 'student_name', 'group_name', 'paymentForm','studentStatus','avg_gpa',)
    search_fields = ('passport_number', 'student_name',)

    def group_name(self, obj):
        try:
            groups = json.loads(obj.groups)
        except Exception:
            groups = obj.groups  

        if isinstance(groups, list) and groups:
            return groups[0].get('name', '-')
        return '-'

admin.site.register(Student, StudentAdmin)
admin.site.register(Criteria)
admin.site.register(StudentFiles)
admin.site.register(Supervisor)
