from django.contrib import admin
from django.urls import path
from . import views

app_name ="myapp"
urlpatterns = [
    path('', views.diary_list, name='diary_list'),
    path('diary_list/', views.diary_list, name='diary_list'),
    path('create/', views.create, name='create'),
    # path('create_content/', views.create_content, name='create_content'),
    path('diary/<int:diary_id>/update/', views.diary_update, name='diary_update'),
    path('diary/<int:diary_id>/delete/', views.diary_delete, name='diary_delete'),
    path("get_content", views.get_content, name="get_content")
]

