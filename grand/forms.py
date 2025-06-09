from django import forms
from .models import StudentFiles

class StudentFilesForm(forms.ModelForm):
    class Meta:
        model = StudentFiles
        fields = ['uploaded_file']

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        self.criteria = kwargs.pop('criteria', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if StudentFiles.objects.filter(student=self.student, criteria=self.criteria).exists():
            raise forms.ValidationError("Siz bu mezon uchun allaqachon fayl yuklagansiz.")
        return cleaned_data
