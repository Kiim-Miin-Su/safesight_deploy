from django.apps import AppConfig  # ✅ 이 줄 추가!

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
