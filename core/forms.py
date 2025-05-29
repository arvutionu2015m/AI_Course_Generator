from django import forms
from .models import Course
from .models import QuizAnswer

class QuizAnswerForm(forms.ModelForm):
    class Meta:
        model = QuizAnswer
        fields = ['user_answer']
        widgets = {
            'user_answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['topic']
