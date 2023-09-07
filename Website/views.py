from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta

from .forms import TaskEditForm, DeliveryEditForm
from .models import Task, Delivery, Day, Return


def get_current_date():
    current_date = datetime.now()
    return current_date


def get_employee_rating(user):
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
    user_rating = get_employee_rating(user)
    current_date = get_current_date()
    day_name = current_date.strftime('%A')

    all_tasks = Task.objects.filter(task_date=current_date).order_by('status', '-is_important', 'creation_time')
    all_tasks_for_dashboard = all_tasks[:5]

    all_tasks_for_user = Task.objects.filter(task_date=current_date, assigned_to__user=user).order_by('status',
                                                                                                      '-is_important',
                                                                                                      'creation_time')
    all_tasks_for_user_dashboard = all_tasks_for_user[:5]

    all_delivery = Delivery.objects.filter(delivery_date=current_date).order_by('-status', 'creation_time')
    delivery_for_dashboard = all_delivery[:5]

    all_returns = Return.objects.filter(return_date=current_date).order_by('-status', 'creation_time')
    returns_for_dashboard = all_returns[:3]

    def get_progress_bar_data(all_tasks, all_delivery, all_returns):
        """
        Calculate progress bar data based on tasks deliveries and returns.

        This function calculates progress bar data for tasks deliveries and returns by determining the total number
        of tasks deliveries and returns to be done, the number of completed tasks deliveries and returns,
        and the percentage of completion.

        Args:
        all_tasks (QuerySet): Queryset of all tasks.
        all_delivery (QuerySet): Queryset of all deliveries.
        all_returns (QuerySet): Queryset of all returns.

        Returns:
        dict: A dictionary containing progress bar data with keys:
        - 'all_to_do': Total count of tasks deliveries and returns to be done.
        - 'all_done': Total count of completed tasks deliveries and returns.
        - 'percentage_done': Percentage of completion.
        """

        all_to_do = all_tasks.count() + all_delivery.count() + all_returns.count()
        progress_tasks_done = all_tasks.filter(status="Zrobione")
        progress_delivery_done = all_delivery.filter(status__in=["Odebrana", "Nie dostarczona"])
        progress_returns_done = all_returns.filter(status="Odebrany")
        all_done = progress_tasks_done.count() + progress_delivery_done.count() + progress_returns_done.count()

        def calculate_percentage(x, y):
            if y == 0:
                return 100  # Avoid division by zero
            percentage = (x / y) * 100
            return int(round(percentage, 0))

        percentage_done = calculate_percentage(all_done, all_to_do)

        progress_bar_data = {
            'all_to_do': all_to_do,
            'all_done': all_done,
            'percentage_done': percentage_done,
        }
        return progress_bar_data

    progress_bar_data = get_progress_bar_data(all_tasks, all_delivery, all_returns)

    def get_progress_bar_data_for_user(all_tasks_for_user, all_delivery, all_returns):
        """
        Calculate progress bar data based on tasks deliveries and returns for specific logged user.

        This function calculates progress bar data for tasks deliveries and returns by determining the total number
        of tasks deliveries and returns to be done, the number of completed tasks deliveries and returns,
        and the percentage of completion.

        Args:
        all_tasks_for_user (QuerySet): Queryset of all tasks for specific logged user.
        all_delivery (QuerySet): Queryset of all deliveries.
        all_returns (QuerySet): Queryset of all returns.

        Returns:
        dict: A dictionary containing progress bar data with keys:
        - 'all_to_do': Total count of tasks deliveries and returns to be done.
        - 'all_done': Total count of completed tasks deliveries and returns.
        - 'percentage_done': Percentage of completion.
        """

        all_to_do = all_tasks_for_user.count() + all_delivery.count() + all_returns.count()
        progress_tasks_done = all_tasks_for_user.filter(status="Zrobione")
        progress_delivery_done = all_delivery.filter(status__in=["Odebrana", "Nie dostarczona"])
        progress_returns_done = all_returns.filter(status="Odebrany")
        all_done = progress_tasks_done.count() + progress_delivery_done.count() + progress_returns_done.count()

        def calculate_percentage(x, y):
            if y == 0:
                return 100  # Avoid division by zero
            percentage = (x / y) * 100
            return int(round(percentage, 0))

        percentage_done = calculate_percentage(all_done, all_to_do)

        progress_bar_data = {
            'all_to_do': all_to_do,
            'all_done': all_done,
            'percentage_done': percentage_done,
        }
        return progress_bar_data

    progress_bar_data_for_user = get_progress_bar_data_for_user(all_tasks_for_user, all_delivery, all_returns)

    def get_end_of_work_hour():
        """
        Get the end of work hour for the current day.

        Returns:
        time: The end of work hour for the current day.
        """

        try:
            current_day = Day.objects.get(day_date=current_date)
            end_of_work_hour = current_day.end_of_work_hour
            return end_of_work_hour
        except Day.DoesNotExist:
            return None

    end_of_work_hour = get_end_of_work_hour()

    context = {
        'user': user,
        'current_date': current_date,
        'day_name': day_name,
        'all_tasks': all_tasks,
        'all_tasks_for_dashboard': all_tasks_for_dashboard,
        'all_tasks_for_user': all_tasks_for_user,
        'all_tasks_for_user_dashboard': all_tasks_for_user_dashboard,
        'user_rating': user_rating,
        'all_delivery': all_delivery,
        'delivery_for_dashboard': delivery_for_dashboard,
        'progress_bar_data': progress_bar_data,
        'progress_bar_data_for_user': progress_bar_data_for_user,
        'end_of_work_hour': end_of_work_hour,
        'all_returns': all_returns,
        'returns_for_dashboard': returns_for_dashboard,

    }
    return render(request, "dashboard.html", context)


@login_required(login_url='login_user')
def task(request):
    user = request.user
    user_rating = get_employee_rating(user)
    current_date = get_current_date()
    all_tasks = Task.objects.filter(task_date=current_date).order_by('status', '-is_important', 'creation_time')
    all_tasks_for_user = Task.objects.filter(task_date=current_date, assigned_to__user=user).order_by('status',
                                                                                                      '-is_important',
                                                                                                      'creation_time')

    if request.method == 'POST':
        selected_day = request.POST.get('selected_day')
        selected_month_and_year = request.POST.get('selected_month')
        selected_month, selected_year = selected_month_and_year.split(' ', 1)

        months = dict(Styczeń='01', Luty='02', Marzec='03', Kwiecień='04', Maj='05', Czerwiec='06', Lipiec='07',
                      Sierpień='08', Wrzesień='09', Październik='10', Listopad='11', Grudzień='12', )

        selected_month = months[selected_month]
        filtered_date = selected_year + '-' + selected_month + '-' + selected_day

        if user.userprofile.position == 'Pracownik':
            filtered_tasks = Task.objects.filter(task_date=filtered_date, assigned_to__user=user).order_by('status',
                                                                                                           '-is_important',
                                                                                                           'creation_time')
            tasks_data = []
            for task in filtered_tasks:
                tasks_data.append({
                    'id': task.id,
                    'name': task.name,
                    'description': task.description,
                    'status': task.status,
                    'is_important': task.is_important,
                })

            return JsonResponse({'filtered_tasks': tasks_data, 'position': 'pracownik'})

        else:
            filtered_tasks = Task.objects.filter(task_date=filtered_date).order_by('status', '-is_important',
                                                                                   'creation_time')
            tasks_data = []
            for task in filtered_tasks:
                tasks_data.append({
                    'id': task.id,
                    'name': task.name,
                    'description': task.description,
                    'status': task.status,
                    'is_important': task.is_important,
                    'assigned_to': task.assigned_to.user.userprofile.profile_picture.url,
                })

            return JsonResponse({'filtered_tasks': tasks_data})

    context = {
        'user': user,
        'user_rating': user_rating,
        'all_tasks': all_tasks,
        'all_tasks_for_user': all_tasks_for_user,
        'current_date': current_date,
    }
    return render(request, "task.html", context)


@login_required(login_url='login_user')
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    current_date = get_current_date()
    user = request.user
    task_edit_form = TaskEditForm(request.POST, instance=task)

    if request.method == 'POST':
        if 'task_edited' in request.POST:
            if task_edit_form.is_valid():
                task_edit_form.save()
                messages.success(request, 'Zadanie zostało zedytowane!')
                return redirect('task_detail_view', task_id=task_id)

        if 'task_done' in request.POST:
            task.status = 'Zrobione'
            task.save()
            messages.success(request, 'Zadanie oznaczone jako wykonane!')
            return redirect('dashboard')

        if 'task_delete' in request.POST:
            task.delete()
            return redirect('dashboard')

    else:
        task_edit_form = TaskEditForm(instance=task)

    context = {
        'task': task,
        'current_date': current_date,
        'user': user,
        'task_edit_form': task_edit_form,
    }

    return render(request, 'task_detail.html', context)


@login_required(login_url='login_user')
def delivery(request):
    user = request.user
    user_rating = get_employee_rating(user)
    current_date = get_current_date()
    all_delivery = Delivery.objects.filter(delivery_date=current_date).order_by('-status', 'creation_time')

    if request.method == 'POST':
        selected_day = request.POST.get('selected_day')
        selected_month_and_year = request.POST.get('selected_month')
        selected_month, selected_year = selected_month_and_year.split(' ', 1)

        months = dict(Styczeń='01', Luty='02', Marzec='03', Kwiecień='04', Maj='05', Czerwiec='06', Lipiec='07',
                      Sierpień='08', Wrzesień='09', Październik='10', Listopad='11', Grudzień='12', )

        selected_month = months[selected_month]
        filtered_date = selected_year + '-' + selected_month + '-' + selected_day

        filtered_delivery = Delivery.objects.filter(delivery_date=filtered_date).order_by('-status', 'creation_time')
        delivery_data = []
        for delivery in filtered_delivery:
            delivery_data.append({
                'id': delivery.id,
                'delivery_company': delivery.delivery_company,
                'form': delivery.form,
                'quantity': delivery.quantity,
                'description': delivery.description,
                'status': delivery.status,
            })

        return JsonResponse({'filtered_delivery': delivery_data})

    context = {
        'user': user,
        'user_rating': user_rating,
        'all_delivery': all_delivery,
        'current_date': current_date,
    }
    return render(request, "delivery.html", context)


@login_required(login_url='login_user')
def delivery_detail_view(request, delivery_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    current_date = get_current_date()
    user = request.user
    delivery_edit_form = DeliveryEditForm(request.POST, instance=delivery)

    if request.method == 'POST':
        if 'delivery_received' in request.POST:
            delivery.status = 'Odebrana'
            delivery.save()
            messages.success(request, 'Dostawa oznaczona jako odebrana!')
            return redirect('dashboard')

        if 'delivery_not_delivered' in request.POST:
            delivery.status = 'Nie dostarczona'
            delivery.save()
            miesiace = [
                'stycznia', 'lutego', 'marca', 'kwietnia',
                'maja', 'czerwca', 'lipca', 'sierpnia',
                'września', 'października', 'listopada', 'grudnia'
            ]
            formatted_data = f"{delivery.delivery_date.day:02d} {miesiace[delivery.delivery_date.month - 1]} {delivery.delivery_date.year}"

            next_day = delivery.delivery_date + timedelta(days=1)
            next_monday = delivery.delivery_date + timedelta(days=2)

            if delivery.delivery_date.strftime("%A") == "Saturday":
                new_delivery = Delivery.objects.create(
                    delivery_company=delivery.delivery_company,
                    form=delivery.form,
                    quantity=delivery.quantity,
                    description=delivery.description,
                    status='W drodze',  # Możesz ustawić domyślny status
                    delivery_date=next_monday,
                    generated_context=f'Dostawa automatycznie przeniesiona z dnia {formatted_data}.',
                )
                new_delivery.save()
            else:
                new_delivery = Delivery.objects.create(
                    delivery_company=delivery.delivery_company,
                    form=delivery.form,
                    quantity=delivery.quantity,
                    description=delivery.description,
                    status='W drodze',  # Możesz ustawić domyślny status
                    delivery_date=next_day,
                    generated_context=f'Dostawa automatycznie przeniesiona z dnia {formatted_data}.',
                )
                new_delivery.save()

            messages.success(request, 'Dostawa została automatycznie dodana do następnego dnia!')
            return redirect('dashboard')

        if 'delivery_edited' in request.POST:
            if delivery_edit_form.is_valid():
                delivery_edit_form.save()
                messages.success(request, 'Dostawa została zedytowana!')
                return redirect('delivery_detail_view', delivery_id=delivery_id)

        if 'delivery_delete' in request.POST:
            delivery.delete()
            return redirect('dashboard')

    else:
        delivery_edit_form = DeliveryEditForm(instance=delivery)

    context = {
        'delivery': delivery,
        'current_date': current_date,
        'user': user,
        'delivery_edit_form': delivery_edit_form,
    }

    return render(request, 'delivery_detail.html', context)
