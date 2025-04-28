# accounts/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/tasks/select/')  # 로그인 후 이동
    else:
        form = AuthenticationForm()
    return render(request, "accounts/log_in.html", {"form": form})
