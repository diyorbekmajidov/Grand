from django import forms
from .models import StudentFiles, validate_img_size

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
    
class StudentFileForm(forms.ModelForm):
    uploaded_file = forms.FileField(required=True)

    class Meta:
        model = StudentFiles
        fields = ['uploaded_file']

    def clean_uploaded_file(self):
        file = self.cleaned_data.get('uploaded_file')
        validate_img_size(file)  # 5 MB limit
        return file
