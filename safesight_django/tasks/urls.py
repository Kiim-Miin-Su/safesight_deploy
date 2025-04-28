# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('select/', views.task_select_view, name='task_select'),
    path('result/', views.task_result_view, name='result'),  # ✅ 여기를 추가
]
