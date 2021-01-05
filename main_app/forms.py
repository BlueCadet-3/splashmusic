from django.forms import ModelForm
from django import forms
from .models import Lesson

class DateInput(forms.DateInput):
    input_type = 'date'

class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['date', 'time', 'instrument', 'description']
        widgets = {
            'date': DateInput(),
        }
