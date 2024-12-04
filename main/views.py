from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from .models import User

def home(request):
    if request.user.is_authenticated:
        user = request.user
        if isinstance(user, User) and user.is_superadmin():
            return redirect('/admin')
        return render(request, 'main/home.html')
    return redirect('/login')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def log_out(request):
    logout(request)
    return redirect('/login')
    # return redirect('/home')

