from rest_framework import serializers
from .models import *
import json

class StudentSerializer(serializers.ModelSerializer):
    group_display = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'student_id_number', 'student_name','faculty', 'phone_number', 'group_display']

    def get_group_display(self, obj):
        return obj.groups[0].get('name', '-')
    
class StudentFilesSerializer(serializers.ModelSerializer):
    criteria_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    faculty_name = serializers.SerializerMethodField()

    class Meta:
        model = StudentFiles
        fields = ['id', 'student', 'task_score', 'is_scored','supervisor', 'supervisor_comment', 'uploaded_file', 'faculty_name','initial_score', 'student_name', 'group_name', 'criteria_name']

    def get_criteria_name(self, obj):
        return obj.criteria.title if obj.criteria else '-'
    
    def get_student_name(self, obj):
        return obj.student.student_name if obj.student else "-"
    
    def get_faculty_name(self, obj):
        return obj.student.faculty if obj.student else "-"
    
    def get_group_name(self, obj):
        try:
            return obj.student.groups[0].get('name', '-')
        except Exception:
            pass
        return "-"