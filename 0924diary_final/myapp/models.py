# Create your models here.
from django.db import models

class Diary2(models.Model):
    content1 = models.TextField()
    content2 = models.TextField()
    content3 = models.TextField()
    todo1 = models.CharField(max_length=200)
    todo2 = models.CharField(max_length=200)
    todo3 = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content1)

    class Meta:
        ordering = ["-date"]  # date 필드를 기준으로 내림차순으로 정렬


from django import forms
from myapp.models import Diary2

class DiaryForm(forms.ModelForm):

    class Meta:
        model = Diary2
        fields = ["content1", "content2", "content3", "todo1", "todo2", "todo3"]
        # fields = "__all__"
        # exclude = ["date"]