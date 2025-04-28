from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # ✅ redirect import 추가

urlpatterns = [
    path('', lambda request: redirect('task_select')),  # ✅ 루트로 오면 작업 선택 페이지로 이동
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
]
