from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from datetime import timedelta
from .models import Task


def get_current_date():
    current_date = datetime.now()
    # today = datetime.today()
    # yesterday = today - timedelta(days=1)
    return current_date


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login_user')

    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url='login_user')
def dashboard(request):
    user = request.user
    current_date = get_current_date()
    print(user.userprofile.profile_picture.url)
    day_name = current_date.strftime('%A')
    tasks = Task.objects.filter(date=current_date).order_by('creation_time')

    context = {
        'user': user,
        'current_date': current_date,
        'day_name': day_name,
        'tasks': tasks,
    }
    return render(request, "dashboard.html", context)
