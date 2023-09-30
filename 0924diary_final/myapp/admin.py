# Register your models here.
from django.contrib import admin
from .models import Diary2

class DiaryAdmin(admin.ModelAdmin):
    search_fields = ['content1']

admin.site.register(Diary2,DiaryAdmin)