from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, ('Invalid username or password'))
            return redirect('login_user')

    else:
        return render(request, 'login.html')


def dashboard(request):
    return render(request, "dashboard.html")
