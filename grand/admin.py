from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources, fields
from .models import Student, Criteria, StudentFiles, Supervisor
import json

# Resource klass
class StudentResources(resources.ModelResource):
    group_name = fields.Field(column_name="groups_name")
    def dehydrate_group_name(self, student):
        try:
            groups = json.loads(student.groups)
        except Exception:
            groups = student.groups  

        if isinstance(groups, list) and groups:
            return groups[0].get('name', '-')
        return '-'
    

    class Meta:
        model = Student
        fields = ('id', 'passport_number', "level", 'phone_number','student_id_number','faculty' ,'student_name', 'group_name', 'paymentForm', 'studentStatus', 'avg_gpa', 'date_created')

# BIRLASHGAN admin klass
@admin.register(Student)
class StudentAdmin(ExportMixin, admin.ModelAdmin):  # asosiy class
    resource_class = StudentResources

    list_display = ('passport_number', 'student_name', 'faculty', 'group_name', 'paymentForm','studentStatus','avg_gpa',)
    search_fields = ('passport_number', 'student_name',)

    def group_name(self, obj):
        try:
            groups = json.loads(obj.groups)
        except Exception:
            groups = obj.groups  

        if isinstance(groups, list) and groups:
            return groups[0].get('name', '-')
        return '-'

    
class StudentFilesAdmin(admin.ModelAdmin):
    list_display = ('student', 'criteria','task_score','initial_score')
    search_fields = ('student__student_name', 'criteria__title',)

# admin.site.register(Student, StudentAdmin)
admin.site.register(Criteria)
admin.site.register(StudentFiles, StudentFilesAdmin)
admin.site.register(Supervisor)
