from django import forms
from .models import Diary2

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary2
        fields = ['content1', 'content2', 'content3', 'todo1', 'todo2', 'todo3']


class MemoForm(forms.ModelForm):
    class Meta:
        model = Diary2
        fields = ['content1', 'content2', 'content3', 'todo1', 'todo2', 'todo3']

