from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import Task, Delivery


def get_current_date():
    current_date = datetime.now()
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
    day_name = current_date.strftime('%A')
    all_tasks = Task.objects.filter(date=current_date).order_by('status', '-is_important', 'creation_time')
    tasks_for_dashboard = all_tasks[:5]

    def get_employee_rating():
        """
            Calculate the user's rating based on completed and assigned tasks.

            This function calculates the user's rating based on the ratio of completed tasks
            to assigned tasks. The rating is scaled to a range from 1 to 5.

            Args:
                user.userprofile (UserProfile): The user's profile containing task information.

            Returns:
                float: The calculated user's rating.

            """
        completed_tasks = user.userprofile.completed_tasks
        assigned_tasks = user.userprofile.assigned_tasks

        if assigned_tasks == 0:
            return 'Brak zadań'

        rating = min(5, max(1, completed_tasks / assigned_tasks * 5))
        return round(rating, 1)

    user_rating = get_employee_rating()

    all_delivery = Delivery.objects.filter(date=current_date).order_by('-status', 'creation_time')
    delivery_for_dashboard = all_delivery[:5]

    def get_progress_bar_data(all_tasks, all_delivery):
        """
           Calculate progress bar data based on tasks and deliveries.

           This function calculates progress bar data for tasks and deliveries by determining
           the total number of tasks and deliveries to be done, the number of completed tasks
           and deliveries, and the percentage of completion.

           Args:
               all_tasks (QuerySet): Queryset of all tasks.
               all_delivery (QuerySet): Queryset of all deliveries.

           Returns:
               dict: A dictionary containing progress bar data with keys:
                   - 'all_to_do': Total count of tasks and deliveries to be done.
                   - 'all_done': Total count of completed tasks and deliveries.
                   - 'percentage_done': Percentage of completion.

        """
        all_to_do = all_tasks.count() + all_delivery.count()
        progress_tasks_done = all_tasks.filter(status="Zrobione")
        progress_delivery_done = all_delivery.filter(status__in=["Odebrana", "Nie dostarczona"])
        all_done = progress_tasks_done.count() + progress_delivery_done.count()

        def calculate_percentage(x, y):
            if y == 0:
                return 0  # Avoid division by zero
            percentage = (x / y) * 100
            return int(round(percentage, 0))

        percentage_done = calculate_percentage(all_done, all_to_do)

        progress_bar_data = {
            'all_to_do': all_to_do,
            'all_done': all_done,
            'percentage_done': percentage_done,
        }
        return progress_bar_data

    progress_bar_data = get_progress_bar_data(all_tasks, all_delivery)
    context = {
        'user': user,
        'current_date': current_date,
        'day_name': day_name,
        'all_tasks': all_tasks,
        'tasks_for_dashboard': tasks_for_dashboard,
        'user_rating': user_rating,
        'all_delivery': all_delivery,
        'delivery_for_dashboard': delivery_for_dashboard,
        'progress_bar_data': progress_bar_data,
    }
    return render(request, "dashboard.html", context)
