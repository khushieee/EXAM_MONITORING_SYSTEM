from django import forms
from admin_panel.models import Exam, TeacherExam

class SelectExamForm(forms.Form):
    exam = forms.ModelChoiceField(queryset=Exam.objects.none())

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super(SelectExamForm, self).__init__(*args, **kwargs)
        if teacher:
            teacher_exams = TeacherExam.objects.filter(teacher=teacher)
            exams_qs = Exam.objects.filter(pk__in=teacher_exams.values('exam'))
            self.fields['exam'].queryset = exams_qs