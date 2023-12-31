from io import BytesIO

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from collections import defaultdict
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

from .forms import TaskEditForm, DeliveryEditForm, ReturnEditForm, OrderItemEditForm, OrderItemCreateForm, \
    StockItemCreateForm, StockItemEditForm, AddDeliveryForm, AddTaskForm, AddReturnForm, DayForm, AddCommentForm
from .models import Task, Delivery, Day, Return, OrderItem, StockItem, UserProfile, Notification, Comment

from reportlab.lib.pagesizes import A6, landscape, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

MONTHS_PL = {
    1: 'styczeń', 2: 'luty', 3: 'marzec', 4: 'kwiecień', 5: 'maj', 6: 'czerwiec',
    7: 'lipiec', 8: 'sierpień', 9: 'wrzesień', 10: 'październik', 11: 'listopad', 12: 'grudzień'
}


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
    progress_returns_done = all_returns.filter(status__in=["Odebrany", "Przygotowany"])
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
    progress_returns_done = all_returns.filter(status__in=["Odebrany", "Przygotowany"])
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


def generate_return_pdf(return_id):
    """
    Generate a PDF file for a given return based on its ID.

    :param return_id: The ID of the return for which the PDF file should be generated.
    :type return_id: int
    :return: HttpResponse containing the PDF file with return data.
    :rtype: HttpResponse
    """
    return_data = get_object_or_404(Return, id=return_id)
    package_quantity = return_data.package_quantity

    # Add a font to PDF
    pdfmetrics.registerFont(TTFont('Poppins_light', 'Website/static/fonts/Poppins_Light_300.ttf'))
    pdfmetrics.registerFont(TTFont('Poppins_bold', 'Website/static/fonts/Poppins_Medium_500.ttf'))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="return_{return_data.name}_{return_data.return_date}.pdf"'

    # Creating a PDF file with ReportLab
    c = canvas.Canvas(response, pagesize=landscape(A6))

    for package_number in range(1, package_quantity + 1):
        c.setFont("Poppins_bold", 15)
        c.drawString(50, 250, 'Awizo: ')
        c.setFont("Poppins_light", 15)
        c.drawString(100, 250, return_data.notice)

        c.setFont("Poppins_bold", 15)
        c.drawString(50, 200, 'Hurtownia: ')
        c.setFont("Poppins_light", 15)
        c.drawString(134, 200, return_data.wholesale)

        c.setFont("Poppins_bold", 15)
        c.drawString(50, 150, 'Data: ')
        c.setFont("Poppins_light", 15)
        c.drawString(93, 150, return_data.return_date.strftime('%d/%m/%Y'))

        c.setFont("Poppins_bold", 15)
        c.drawString(50, 100, 'Uwagi: ')
        c.setFont("Poppins_light", 15)
        c.drawString(103, 100, return_data.notes)

        c.setFont("Poppins_bold", 15)
        c.drawString(50, 50, 'Ilość paczek: ')
        c.setFont("Poppins_light", 15)
        c.drawString(150, 50, f'{package_number}/{package_quantity}')

        if package_number < package_quantity:
            c.showPage()  # Switch to next page

    c.save()

    return response


def add_notification(user, target, notif_name, notif_description):
    """
    Create a notification based on the user, target, notification name, and description.

    Args:
        user (User): The user triggering the notification.
        target (Task or other): The target object for the notification.
        notif_name (str): The name of the notification.
        notif_description (str): The description of the notification.

    Returns:
        None

    Creates a notification with the provided details. If the target is a Task, the notification is
    added for the assigned user. If the target is not a Task, notifications are added for employees
    or designated higher-level positions like 'Szef' or 'Admin' based on the user's position.
    """

    # Check if the target is a Task
    if isinstance(target, Task):
        if user.userprofile.position != 'Pracownik':
            # Create a notification and add it for the assigned user
            notification = Notification.objects.create(
                model_name=notif_name,
                model_id=target.id,
                description=notif_description,
                made_by=user
            )
            notification.notify_for.add(target.assigned_to)
        elif user.userprofile.position == 'Pracownik':
            users = UserProfile.objects.filter(Q(position='Szef') | Q(position='Admin'))
            # Create a notification and add it for the specified users
            notification = Notification.objects.create(
                model_name=notif_name,
                model_id=target.id,
                description=notif_description,
                made_by=user
            )
            for _ in users:
                notification.notify_for.add(_)
    # If the target is not a Task
    else:
        if user.userprofile.position != 'Pracownik':
            users = UserProfile.objects.filter(position='Pracownik')
            # Create a notification and add it for the specified users
            notification = Notification.objects.create(
                model_name=notif_name,
                model_id=target.id,
                description=notif_description,
                made_by=user
            )
            for _ in users:
                notification.notify_for.add(_)

        elif user.userprofile.position == 'Pracownik':
            users = UserProfile.objects.filter(Q(position='Szef') | Q(position='Admin'))
            # Create a notification and add it for the specified users
            notification = Notification.objects.create(
                model_name=notif_name,
                model_id=target.id,
                description=notif_description,
                made_by=user
            )
            for _ in users:
                notification.notify_for.add(_)


def get_notifications(user):
    """
    Retrieves notifications based on the user's profile position.

    Args:
        user (User): The user object.

    Returns:
        tuple: A tuple containing two querysets - unread_notifications and read_notifications.
            unread_notifications (QuerySet): Notifications not yet read for the user's profile.
            read_notifications (QuerySet): Latest 10 notifications that have been read for the user's profile.
    """

    if user.userprofile.position == 'Pracownik':
        # Get notifications that have not yet been read and are for the employee
        unread_notifications = Notification.objects.filter(
            Q(notify_for=user.userprofile) & ~Q(read_by=user.userprofile)
        ).order_by('-creation_time')

        # Get notifications that have been read and are for the employee
        read_notifications = Notification.objects.filter(
            Q(notify_for=user.userprofile) & Q(read_by=user.userprofile)
        ).order_by('-creation_time')[:10]
    else:
        # Get notifications that have not yet been read and are for the employee
        unread_notifications = Notification.objects.filter(
            Q(notify_for=user.userprofile) & ~Q(read_by=user.userprofile)
        ).order_by('-creation_time')

        # Get notifications that have been read and are for the employee
        read_notifications = Notification.objects.filter(
            Q(notify_for=user.userprofile) & Q(read_by=user.userprofile)
        ).order_by('-creation_time')[:10]

    return unread_notifications, read_notifications


class PageNumCanvas(canvas.Canvas):
    """
    Klasa obsługująca numerację stron.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page_num, page in enumerate(self.pages, start=1):
            self.__dict__.update(page)
            self.draw_page_number(page_num, num_pages)
            super().showPage()

        super().save()

    def draw_page_number(self, page_num, total_pages):
        page_text = f"Strona {page_num}/{total_pages}"
        text_width = self.stringWidth(page_text, 'Poppins_light', 10)
        self.setFont('Poppins_light', 10)
        self.drawRightString(587 - text_width, 50, page_text)  # Adjusted coordinates


def generate_stock_items_pdf():
    """
    Generate a PDF containing a list of stock items.

    This function retrieves data from the Django model `StockItem`,
    formats it into a tabular structure, and generates a PDF file with
    appropriate headers, pagination, and formatting.

    Returns:
        HttpResponse: HTTP response with the PDF file as content.
    """

    # Get data from the StockItem model
    stock_items = StockItem.objects.all()

    # Register fonts
    pdfmetrics.registerFont(TTFont('Poppins_light', 'Website/static/fonts/Poppins_Light_300.ttf'))
    pdfmetrics.registerFont(TTFont('Poppins_bold', 'Website/static/fonts/Poppins_Medium_500.ttf'))

    # Define data and headers
    data = [['Nr', 'Nazwa', 'Ilość']]
    lp = 1
    for item in stock_items:
        data.append([str(lp), item.dimensions, str(item.quantity)])
        lp += 1

    left_margin = 50
    right_margin = 50

    # Calculate the page width minus margins
    usable_width = A4[0] - (left_margin + right_margin)

    # Proportionally divide width for columns
    num_columns = 3
    col_widths = [usable_width / num_columns] * num_columns

    # Assign a larger width for the second column
    col_widths[0] = col_widths[0] * 0.24  # Możesz dostosować szerokość według potrzeb
    col_widths[1] = col_widths[1] * 2.4  # Możesz dostosować szerokość według potrzeb
    col_widths[2] = col_widths[2] * 0.28  # Możesz dostosować szerokość według potrzeb

    # Style settings
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Poppins_bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Style for data
    style_data = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Poppins_light'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ])

    # Create a table
    stock_table = Table(data, colWidths=col_widths)
    stock_table.setStyle(style)
    stock_table.setStyle(style_data)

    # Get the current date and format
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Add a style for the title and date
    style_title = ParagraphStyle(
        'CustomTitle',
        parent=getSampleStyleSheet()['Heading1'],
        fontName='Poppins_bold',
        fontSize=15,
        alignment=TA_LEFT,
    )

    style_generated_date = ParagraphStyle(
        'CustomGeneratedDate',
        parent=getSampleStyleSheet()['Normal'],
        fontName='Poppins_light',
        fontSize=10,
        alignment=TA_RIGHT,
    )

    title = Paragraph("Lista przedmiotów na magazynie", style_title)
    generated_date = Paragraph(f"Wygenerowano: {current_date}", style_generated_date)

    # Create content
    content = [title, generated_date, Spacer(1, 10), stock_table, Spacer(1, 10)]

    # Create PDF file in memory
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=50, bottomMargin=50, leftMargin=50, rightMargin=50)
    doc.title = "Lista przedmiotów na magazynie"
    doc.build(content, canvasmaker=PageNumCanvas)

    # Set appropriate headers for automatic downloading
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="stock_items.pdf"'

    # Save the contents of the response buffer
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def generate_delivery_pdf(start_date, end_date):
    """
    Generate a PDF containing a list of delivery from a specific date range.

    This function retrieves data from the Django model `Delivery`,
    formats it into a tabular structure, and generates a PDF file with
    appropriate headers, pagination, and formatting.

    Returns:
        HttpResponse: HTTP response with the PDF file as content.
    """
    delivery = Delivery.objects.filter(delivery_date__range=[start_date, end_date]).order_by('delivery_date')

    if delivery.count() == 0:
        return 0
    else:
        start_date = parse_date(start_date).strftime('%d.%m.%Y')
        end_date = parse_date(end_date).strftime('%d.%m.%Y')

        # Register fonts
        pdfmetrics.registerFont(TTFont('Poppins_light', 'Website/static/fonts/Poppins_Light_300.ttf'))
        pdfmetrics.registerFont(TTFont('Poppins_bold', 'Website/static/fonts/Poppins_Medium_500.ttf'))

        # Create a PDF file
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Dostawy_{start_date}-{end_date}.pdf"'

        # Define data and headers
        data = [['Nr', 'Dostawca', 'Forma', 'Ilość', 'Data', 'Status']]

        lp = 1
        for item in delivery:
            data.append(
                [str(lp), item.delivery_company, item.form, str(item.quantity), str(item.delivery_date), item.status])
            lp += 1

        left_margin = 50
        right_margin = 50

        # Get the current date and format
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Add a style for the title and date
        style_title = ParagraphStyle(
            'CustomTitle',
            parent=getSampleStyleSheet()['Heading1'],
            fontName='Poppins_bold',
            alignment=TA_LEFT,
            fontSize=15,
        )
        style_generated_text = ParagraphStyle(
            'CustomGeneratedText',
            parent=getSampleStyleSheet()['Normal'],
            fontName='Poppins_light',
            fontSize=10,
            alignment=TA_LEFT,
            leftIndent=0,
        )
        style_generated_date = ParagraphStyle(
            'CustomGeneratedDate',
            parent=getSampleStyleSheet()['Normal'],
            fontName='Poppins_light',
            fontSize=10,
            alignment=TA_RIGHT,
            rightIndent=0,
        )

        title = Paragraph("Lista dostaw", style_title)

        # Stworzenie tabeli z dwiema komórkami dla paragrafów (first table)
        text_table_data = [
            [Paragraph(f"Przedział czasowy: {start_date} - {end_date}", style_generated_text),
             Paragraph(f"Wygenerowano: {current_date}", style_generated_date)]
        ]

        # Calculate the page width minus margins (first table)
        usable_width_first_table = A4[0] - (left_margin + right_margin)

        # Proportionally divide width for columns (first table)
        num_columns_first_table = 2
        col_widths_first_table = [usable_width_first_table / num_columns_first_table] * num_columns_first_table

        text_table = Table(text_table_data,
                           colWidths=col_widths_first_table)

        # Set the style for the first table
        text_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ]))

        # Calculate the page width minus margins (second table)
        usable_width_second_table = A4[0] - (left_margin + right_margin)

        # Proportionally divide width for columns (secodnd table)
        num_columns_second_table = 6
        col_widths_second_table = [usable_width_second_table / num_columns_second_table] * num_columns_second_table

        # Assign a larger width for the second column
        col_widths_second_table[0] = col_widths_second_table[0] * 0.54
        col_widths_second_table[1] = col_widths_second_table[1] * 1.2
        col_widths_second_table[2] = col_widths_second_table[2] * 1.1
        col_widths_second_table[3] = col_widths_second_table[3] * 0.6
        col_widths_second_table[4] = col_widths_second_table[4] * 1.2
        col_widths_second_table[5] = col_widths_second_table[5] * 1.2

        # Set the style for the second table
        second_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Poppins_light'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Create a data table (second table)
        stock_table = Table(data, colWidths=col_widths_second_table)
        stock_table.setStyle(second_table_style)

        # Create content
        content = [title, text_table, Spacer(1, 10), stock_table, Spacer(1, 10)]

        # Create PDF file in memory
        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=50, bottomMargin=50, leftMargin=50, rightMargin=50)
        doc.title = "Lista dostaw"
        doc.build(content, canvasmaker=PageNumCanvas)

        # Set appropriate headers for automatic downloading
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Dostawy_{start_date}-{end_date}.pdf"'

        # Save the contents of the response buffer
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


def generate_user_stock_items_pdf():
    """
    Generate a PDF containing a list of stock items for a user.

    This function retrieves data from the Django model `StockItem`,
    formats it into a tabular structure, and generates a PDF file with
    appropriate headers, pagination, and formatting.

    Returns:
        HttpResponse: HTTP response with the PDF file as content.
    """
    # Get data from the StockItem model
    stock_items = StockItem.objects.all()

    pdfmetrics.registerFont(TTFont('Poppins_light', 'Website/static/fonts/Poppins_Light_300.ttf'))
    pdfmetrics.registerFont(TTFont('Poppins_bold', 'Website/static/fonts/Poppins_Medium_500.ttf'))

    # Define data and headers
    data = [['Nr', 'Nazwa', 'Ilość', 'Nd', 'So', 'Pn', 'Wt', 'Śr', 'Cz', 'Pt', 'Suma']]
    lp = 1
    for item in stock_items:
        data.append([str(lp), item.dimensions, str(item.quantity), '', '', '', '', '', '', '', ''])
        lp += 1

    left_margin = 70
    right_margin = 70

    # Calculate the page width minus margins
    usable_width = letter[0] - (left_margin + right_margin)

    # Proportionally divide width for columns
    num_columns = 11
    col_widths = [usable_width / num_columns] * num_columns

    # Assign a larger width for the second column
    col_widths[1] = col_widths[1] * 3

    # Style settings
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Poppins_bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Style for data
    style_data = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Poppins_light'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ])

    # Create a table
    stock_table = Table(data, colWidths=col_widths)
    stock_table.setStyle(style)
    stock_table.setStyle(style_data)

    # Create PDF file in memory
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=20, bottomMargin=20)
    doc.title = "Tygodniowa lista przedmiotów - pracownik"
    doc.build([stock_table])

    # Set appropriate headers for automatic downloading
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="weekly_stock_items.pdf"'

    # Save the contents of the response buffer
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

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
    unread_notifications, read_notifications = get_notifications(request.user)
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

    all_returns = Return.objects.filter(status__in=["Do spakowania", "Przygotowany"]).order_by('status',
                                                                                               'creation_time')
    returns_for_dashboard = all_returns[:2]

    progress_bar_data = get_progress_bar_data(all_tasks, all_delivery, all_returns)

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
        'unread_notifications': unread_notifications,
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
    unread_notifications, read_notifications = get_notifications(request.user)
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
        'unread_notifications': unread_notifications,
        'user_rating': user_rating,
        'all_tasks': all_tasks,
        'all_tasks_for_user': all_tasks_for_user,
        'current_date': current_date,
    }

    return render(request, "task.html", context)


@login_required(login_url='login_user')
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task_comments = Comment.objects.filter(model_id=task.id, model_name='Zadanie').order_by('-creation_time')
    current_date = get_current_date()
    user = request.user
    unread_notifications, read_notifications = get_notifications(request.user)
    user_rating = get_employee_rating(user)
    task_edit_form = TaskEditForm(request.POST, instance=task)
    task_comment_form = AddCommentForm()

    if request.method == 'POST':
        if 'task_edited' in request.POST:
            if task_edit_form.is_valid():
                instance = task_edit_form.save()
                add_notification(request.user, instance, 'Zadanie', 'Zadanie zostało zedytowane!')
                messages.success(request, 'Zadanie zostało zedytowane!')
                return redirect('task_detail_view', task_id=task_id)

        if 'task_done' in request.POST:
            task.status = 'Zrobione'
            task.save()
            user.userprofile.completed_tasks += 1
            user.userprofile.save()

            add_notification(request.user, task, 'Zadanie', 'Status zadania został zmieniony na "Zrobione"!')
            messages.success(request, 'Zadanie oznaczone jako wykonane!')
            return redirect('dashboard')

        if 'task_delete' in request.POST:
            add_notification(request.user, task, 'Zadanie', 'Zadanie zostało usunięte!')
            task.delete()
            return redirect('dashboard')
        if 'add_comment' in request.POST:
            form = AddCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.model_id = task.id
                comment.model_name = 'Zadanie'
                comment.added_by = request.user.userprofile
                comment.save()
                task.comments.add(comment)
                add_notification(request.user, task, 'Komentarz', 'Nowy komentarz do zadania został dodany!')
                messages.success(request, 'Komentarz został dadany!')
                return redirect('task_detail_view', task_id=task_id)

    else:
        task_edit_form = TaskEditForm(instance=task)

    context = {
        'task': task,
        'task_comments': task_comments,
        'unread_notifications': unread_notifications,
        'current_date': current_date,
        'user': user,
        'user_rating': user_rating,
        'task_edit_form': task_edit_form,
        'task_comment_form': task_comment_form,
    }

    return render(request, 'task_detail.html', context)


@login_required(login_url='login_user')
def delivery(request):
    user = request.user
    unread_notifications, read_notifications = get_notifications(request.user)
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
        'unread_notifications': unread_notifications,
        'user_rating': user_rating,
        'all_delivery': all_delivery,
        'current_date': current_date,
    }

    return render(request, "delivery.html", context)


@login_required(login_url='login_user')
def delivery_detail_view(request, delivery_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    delivery_comments = Comment.objects.filter(model_id=delivery.id, model_name='Dostawa').order_by('-creation_time')
    current_date = get_current_date()
    user = request.user
    unread_notifications, read_notifications = get_notifications(request.user)
    user_rating = get_employee_rating(user)
    delivery_edit_form = DeliveryEditForm(request.POST, request.FILES, instance=delivery)
    delivery_comment_form = AddCommentForm()

    if request.method == 'POST':
        if 'delivery_received' in request.POST:
            delivery.status = 'Odebrana'
            delivery.save()
            add_notification(request.user, delivery, 'Dostawa', 'Status dostawy został zmieniony na "Odebrana"!')
            messages.success(request, 'Dostawa oznaczona jako odebrana!')
            return redirect('dashboard')

        if 'delivery_not_delivered' in request.POST:
            delivery.status = 'Nie dostarczona'
            delivery.save()
            add_notification(request.user, delivery, 'Dostawa', 'Status dostawy został zmieniony na "Nie dostarczona"!')

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
            print(request.FILES)
            if delivery_edit_form.is_valid():
                instance = delivery_edit_form.save()
                add_notification(request.user, instance, 'Dostawa', 'Dostawa została zedytowana!')
                messages.success(request, 'Dostawa została zedytowana!')
                return redirect('delivery_detail_view', delivery_id=delivery_id)

        if 'delivery_delete' in request.POST:
            add_notification(request.user, delivery, 'Dostawa', 'Dostawa została usunięta!')
            delivery.delete()
            return redirect('dashboard')

        if 'add_comment' in request.POST:
            form = AddCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.model_id = delivery.id
                comment.model_name = 'Dostawa'
                comment.added_by = request.user.userprofile
                comment.save()
                delivery.comments.add(comment)
                add_notification(request.user, delivery, 'Komentarz', 'Nowy komentarz do dostawy został dodany!')
                messages.success(request, 'Komentarz został dadany!')
                return redirect('delivery_detail_view', delivery_id=delivery_id)

    else:
        delivery_edit_form = DeliveryEditForm(instance=delivery)

    context = {
        'delivery': delivery,
        'delivery_comments': delivery_comments,
        'current_date': current_date,
        'user': user,
        'unread_notifications': unread_notifications,
        'user_rating': user_rating,
        'delivery_edit_form': delivery_edit_form,
        'delivery_comment_form': delivery_comment_form,
    }

    return render(request, 'delivery_detail.html', context)


@login_required(login_url='login_user')
def returns(request):
    user = request.user
    unread_notifications, read_notifications = get_notifications(request.user)
    user_rating = get_employee_rating(user)
    current_date = get_current_date()

    active_returns = Return.objects.filter(status__in=["Do spakowania", "Przygotowany"]).order_by('status',
                                                                                                  'return_date')

    received_returns = Return.objects.filter(status="Odebrany").order_by('status', '-return_date')

    search_query = request.GET.get('q')
    if search_query:
        # Check if the entered query is a number
        if search_query.isdigit():
            # If the query is a number, try to convert it to an integer
            search_query_int = int(search_query)
            received_returns = received_returns.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(return_date__day=search_query_int) |
                Q(return_date__month=search_query_int) |
                Q(return_date__year=search_query_int)
            )
        else:
            # If the query is not a number, treat it as a text search
            received_returns = received_returns.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

    paginator_received = Paginator(received_returns, 5)  # Show 5 items per page
    page_number_received = request.GET.get('page_received')
    page_received = paginator_received.get_page(page_number_received)

    paginator_active = Paginator(active_returns, 5)  # Show 5 items per page
    page_number_active = request.GET.get('page_active')
    page_active = paginator_active.get_page(page_number_active)

    context = {
        'user': user,
        'unread_notifications': unread_notifications,
        'user_rating': user_rating,
        'active_returns': active_returns,
        'received_returns': received_returns,
        'current_date': current_date,
        'page_received': page_received,
        'page_active': page_active,
        'search_query': search_query,
    }

    return render(request, "return.html", context)


@login_required(login_url='login_user')
def returns_detail_view(request, return_id):
    return_detail = get_object_or_404(Return, id=return_id)
    current_date = get_current_date()
    user = request.user
    unread_notifications, read_notifications = get_notifications(request.user)
    user_rating = get_employee_rating(user)
    return_edit_form = ReturnEditForm(request.POST, instance=return_detail)

    if request.method == 'POST':
        if 'return_packed' in request.POST:
            return_detail.status = 'Przygotowany'
            return_detail.save()
            add_notification(request.user, return_detail, 'Zwrot', 'Status zwrotu został zmieniony na "Przygotowany"!')
            messages.success(request, 'Zwrot oznaczony jako przygotowany!')
            return redirect('dashboard')

        if 'return_received' in request.POST:
            return_detail.status = 'Odebrany'
            return_detail.save()
            add_notification(request.user, return_detail, 'Zwrot', 'Status zwrotu został zmieniony na "Odebrany"!')
            messages.success(request, 'Zwrot oznaczony jako odebrany!')
            return redirect('dashboard')

        if 'generate_notice' in request.POST:
            return_pdf_response = generate_return_pdf(return_id)
            return return_pdf_response

        if 'return_edited' in request.POST:
            if return_edit_form.is_valid():
                instance = return_edit_form.save()
                add_notification(request.user, instance, 'Zwrot', 'Zwrot został zedytowany!')
                messages.success(request, 'Zwrot został zedytowany!')
                return redirect('returns_detail_view', return_id=return_id)

        if 'return_delete' in request.POST:
            add_notification(request.user, return_detail, 'Zwrot', 'Zwrot został usunięty!')
            return_detail.delete()
            return redirect('dashboard')

    else:
        return_edit_form = ReturnEditForm(instance=return_detail)

    context = {
        'return_detail': return_detail,
        'current_date': current_date,
        'user': user,
        'unread_notifications': unread_notifications,
        'user_rating': user_rating,
        'return_edit_form': return_edit_form,
    }

    return render(request, 'return_detail.html', context)


@login_required(login_url='login_user')
def order_item(request):
    user = request.user
    unread_notifications, read_notifications = get_notifications(request.user)
    user_rating = get_employee_rating(user)
    create_order_item_form = OrderItemCreateForm(request.POST)

    items_to_order = OrderItem.objects.all().order_by('status', '-creation_time')

    search_query = request.GET.get('q')
    if search_query:
        items_to_order = items_to_order.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    paginator = Paginator(items_to_order, 14)  # Show 10 items per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.method == 'POST':
        if 'order_item_create' in request.POST:
            form = OrderItemCreateForm(request.POST)
            if form.is_valid():
                order_item = form.save(commit=False)
                order_item.created_by = request.user
                order_item.save()
                add_notification(request.user, order_item, 'Zamówienie', 'Nowy przedmiot do zamówienia został dodany!')
                messages.success(request, 'Przedmiot został dodany!')
                return redirect('order_item')

        if 'change_status' in request.POST:
            item_id = request.POST.get('item_id')
            new_status = request.POST.get('new_status')
            # Retrieve the OrderItem
            item = OrderItem.objects.get(id=item_id)
            item.status = new_status
            item.save()
            add_notification(request.user, item, 'Zamówienie', 'Status przedmiotu do zamówienia został zmieniony!')

    else:
        create_order_item_form = OrderItemCreateForm()

    context = {
        'user': user,
        'unread_notifications': unread_notifications,
        'user_rating': user_rating,
        'items_to_order': items_to_order,
        'page': page,
        'create_order_item_form': create_order_item_form,
        'search_query': search_query,
    }

    return render(request, "order_item.html", context)


@login_required(login_url='login_user')
def order_item_detail_view(request, order_item_id):
    order_item_detail = get_object_or_404(OrderItem, id=order_item_id)
    current_date = get_current_date()
    user = request.user
    unread_notifications, read_notifications = get_notifications(request.user)
    user_rating = get_employee_rating(user)
    order_item_edit_form = OrderItemEditForm(request.POST, instance=order_item_detail)

    if request.method == 'POST':
        if 'order_item_ordered' in request.POST:
            order_item_detail.status = 'Zamówione'
            order_item_detail.save()
            add_notification(request.user, order_item_detail, 'Zamówienie',
                             'Status przedmiotu do zamówienia został zmieniony na "Zamówione"!')
            messages.success(request, 'Produkt oznaczony jako zamówiony!')
            return redirect('order_item_detail_view', order_item_id=order_item_detail.id)

        if 'order_item_not_available' in request.POST:
            order_item_detail.status = 'Niedostępne'
            order_item_detail.save()
            add_notification(request.user, order_item_detail, 'Zamówienie',
                             'Status przedmiotu do zamówienia został zmieniony na "Niedostępne"!')
            messages.success(request, 'Produkt oznaczony jako niedostępny!')
            return redirect('order_item_detail_view', order_item_id=order_item_detail.id)

        if 'order_item_edited' in request.POST:
            if order_item_edit_form.is_valid():
                instance = order_item_edit_form.save()
                add_notification(request.user, instance, 'Zamówienie', 'Przedmiot do zamówienia został zedytowany!')
                messages.success(request, 'Przedmiot został zedytowany!')
                return redirect('order_item_detail_view', order_item_id=order_item_detail.id)

        if 'order_item_delete' in request.POST:
            add_notification(request.user, order_item_detail, 'Zamówienie', 'Przedmiot do zamówienia został usunięty!')
            order_item_detail.delete()
            return redirect('order_item')

    else:
        order_item_edit_form = OrderItemEditForm(instance=order_item_detail)

    context = {
        'order_item_detail': order_item_detail,
        'current_date': current_date,
        'user': user,
        'unread_notifications': unread_notifications,
        'user_rating': user_rating,
        'order_item_edit_form': order_item_edit_form,
    }

    return render(request, 'order_item_detail.html', context)


@login_required(login_url='login_user')
def stock_item(request):
    user = request.user
    unread_notifications, read_notifications = get_notifications(request.user)
    user_rating = get_employee_rating(user)
    stock_items = StockItem.objects.all().order_by('quantity')
    create_stock_item_form = StockItemCreateForm(request.POST)

    search_query = request.GET.get('q')
    if search_query:
        stock_items = stock_items.filter(
            Q(dimensions__icontains=search_query) | Q(usage__icontains=search_query)
        )

    paginator = Paginator(stock_items, 14)  # Show 10 items per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.method == 'POST':
        if 'stock_item_create' in request.POST:
            form = StockItemCreateForm(request.POST)
            form.created_by = request.user
            if form.is_valid():
                stock_item = form.save(commit=False)
                stock_item.created_by = request.user
                stock_item.save()
                add_notification(request.user, stock_item, 'Magazyn', 'Nowy przedmiot na magazynie został dodany!')
                messages.success(request, 'Przedmiot został dodany!')
                return redirect('stock_item')

        if 'stock_item_increase_quantity' in request.POST:
            item_id = request.POST.get('increase_item_id')
            quantity = int(request.POST.get('increase_quantity'))

            # Find the right item and increase the quantity
            item = StockItem.objects.get(id=item_id)
            item.quantity += quantity
            item.save()
            add_notification(request.user, item, 'Magazyn', 'Ilość przedmiotu na magazynie została zwiększona!')
            messages.success(request, 'Ilość przedmiotu została zwiększona!')
            return redirect('stock_item')

        if 'stock_item_reduce_quantity' in request.POST:
            item_id = request.POST.get('reduce_item_id')

            quantity = int(request.POST.get('reduce_quantity'))

            # Find the right item and reduce the quantity
            item = StockItem.objects.get(id=item_id)
            item.quantity -= quantity
            item.save()
            add_notification(request.user, item, 'Magazyn', 'Ilość przedmiotu na magazynie została zmniejszona!')
            messages.success(request, 'Ilość przedmiotu została zmniejszona!')
            return redirect('stock_item')

        if 'generate_user_stock_items_pdf' in request.POST:
            user_stock_items_pdf = generate_user_stock_items_pdf()
            return user_stock_items_pdf
    else:
        create_stock_item_form = StockItemCreateForm()

    context = {
        'user': user,
        'unread_notifications': unread_notifications,
        'user_rating': user_rating,
        'stock_items': stock_items,
        'page': page,
        'search_query': search_query,
        'create_stock_item_form': create_stock_item_form,
    }

    return render(request, 'stock_item.html', context)


@login_required(login_url='login_user')
def stock_item_detail_view(request, stock_item_id):
    stock_item_detail = get_object_or_404(StockItem, id=stock_item_id)
    current_date = get_current_date()
    user = request.user
    unread_notifications, read_notifications = get_notifications(request.user)
    user_rating = get_employee_rating(user)
    stock_item_edit_form = StockItemEditForm(request.POST, instance=stock_item_detail)

    if request.method == 'POST':
        if 'stock_item_increase_quantity' in request.POST:
            increase_quantity_value = int(request.POST.get('increase_quantity_value'))
            stock_item_detail.quantity += increase_quantity_value
            stock_item_detail.save()
            add_notification(request.user, stock_item_detail, 'Magazyn',
                             'Ilość przedmiotu na magazynie została zwiększona!')
            messages.success(request, 'Ilość przedmiotu została zwiększona!')
            return redirect('stock_item_detail_view', stock_item_id=stock_item_detail.id)

        if 'stock_item_reduce_quantity' in request.POST:
            reduce_quantity_value = int(request.POST.get('reduce_quantity_value'))
            stock_item_detail.quantity -= reduce_quantity_value
            stock_item_detail.save()
            add_notification(request.user, stock_item_detail, 'Magazyn',
                             'Ilość przedmiotu na magazynie została zmniejszona!')
            messages.success(request, 'Ilość przedmiotu została zmniejszona!')
            return redirect('stock_item_detail_view', stock_item_id=stock_item_detail.id)

        if 'stock_item_edited' in request.POST:
            if stock_item_edit_form.is_valid():
                instance = stock_item_edit_form.save()
                add_notification(request.user, instance, 'Magazyn', 'Przedmiot na magazynie został zedytowany!')
                messages.success(request, 'Przedmiot został zedytowany!')
                return redirect('stock_item_detail_view', stock_item_id=stock_item_detail.id)

        if 'stock_item_delete' in request.POST:
            add_notification(request.user, stock_item_detail, 'Magazyn', 'Przedmiot na magazynie został usunięty!')
            stock_item_detail.delete()
            return redirect('stock_item')

    else:
        stock_item_edit_form = StockItemEditForm(instance=stock_item_detail)

    context = {
        'stock_item_detail': stock_item_detail,
        'current_date': current_date,
        'user': user,
        'unread_notifications': unread_notifications,
        'user_rating': user_rating,
        'stock_item_edit_form': stock_item_edit_form,
    }

    return render(request, 'stock_item_detail.html', context)


@login_required(login_url='login_user')
def admin_panel(request):
    all_workers = UserProfile.objects.all().filter(position='Pracownik')
    current_date = get_current_date()
    unread_notifications, read_notifications = get_notifications(request.user)

    def get_workers_rating_in_dict(all_workers):
        """
        Function to calculate worker ratings based on completed and assigned tasks.

        Parameters:
            all_workers (list): List of worker objects containing information about completed and assigned tasks.

        Returns:
            dict: A dictionary containing worker ratings, where the key is the worker's username,
                  and the value is the rating on a scale from 1 to 5 (rounded to one decimal place)
                  or 'No tasks' if the worker has no assigned tasks.
        """

        workers_rating = {}
        for worker in all_workers:
            completed_tasks = worker.completed_tasks
            assigned_tasks = worker.assigned_tasks

            if assigned_tasks == 0:
                workers_rating[worker.user.username] = 'Brak zadań'
                continue

            rating = round(min(5, max(1, completed_tasks / assigned_tasks * 5)), 1)
            workers_rating[worker.user.username] = rating

        return workers_rating

    def get_deliveries_count_last_six_months():
        """
        Get the count of deliveries for each month in the last six months.

        Returns:
        month_labels (list): List of month labels for the last six months.
        month_data (list): List of delivery counts for each month.
        """
        today = timezone.now()
        six_months_ago = today - timedelta(days=180)  # 6 months ago

        # Group deliveries by months and count the number of deliveries for each month
        deliveries = Delivery.objects.filter(
            delivery_date__gte=six_months_ago,
            delivery_date__lte=today
        )

        # Create a dictionary with data on the number of deliveries for each month
        data = defaultdict(int)
        for delivery in deliveries:
            # Extract year and month from the delivery date
            year_month = delivery.delivery_date.strftime('%Y-%m')
            data[year_month] += 1

        # Get the full range of months from 6 months ago to the current month
        month = today.month
        year = today.year
        month_labels = []
        month_data = []

        for i in range(6):
            month_labels.append(MONTHS_PL[month] if month in MONTHS_PL else f'Unknown Month ({month})')
            month_data.append(data.get(f'{year}-{month:02}', 0))
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        return month_labels, month_data

    def get_tasks_count_last_six_months():
        """
        Get the count of tasks for each month in the last six months.

        Returns:
        month_labels (list): List of month labels for the last six months.
        month_data (list): List of task counts for each month.
        """
        today = timezone.now()
        six_months_ago = today - timedelta(days=180)  # 6 months ago

        # Group tasks by months and count the number of tasks for each month
        tasks = Task.objects.filter(
            task_date__gte=six_months_ago,
            task_date__lte=today
        )

        # Create a dictionary with data on the number of tasks for each month
        data = defaultdict(int)
        for task in tasks:
            # Extract year and month from the task date
            year_month = task.task_date.strftime('%Y-%m')
            data[year_month] += 1

        # Get the full range of months from 6 months ago to the current month
        month = today.month
        year = today.year
        month_labels = []
        month_data = []

        for i in range(6):
            month_labels.append(MONTHS_PL[month] if month in MONTHS_PL else f'Unknown Month ({month})')
            month_data.append(data.get(f'{year}-{month:02}', 0))
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        return month_labels, month_data

    workers_rating_dictionary = get_workers_rating_in_dict(all_workers)
    delivery_month_labels, delivery_month_data = get_deliveries_count_last_six_months()
    tasks_month_labels, tasks_month_data = get_tasks_count_last_six_months()

    add_delivery_form = AddDeliveryForm()
    add_task_form = AddTaskForm()
    add_return_form = AddReturnForm()
    day_form = DayForm()

    if request.method == 'POST':
        if 'add_delivery' in request.POST:
            form = AddDeliveryForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save()
                add_notification(request.user, instance, 'Dostawa', 'Nowa dostawa została dodana!')
                messages.success(request, 'Dostawa została utworzona!')
                return redirect('admin_panel')

        if 'add_task' in request.POST:
            form = AddTaskForm(request.POST)
            if form.is_valid():
                instance = form.save()
                assigned_user = UserProfile.objects.get(user__username=instance.assigned_to)
                assigned_user.assigned_tasks += 1
                assigned_user.save()
                add_notification(request.user, instance, 'Zadanie', 'Nowe zadanie zostało dodane!')
                messages.success(request, 'Zadanie zostało utworzone!')
                return redirect('admin_panel')

        if 'add_return' in request.POST:
            form = AddReturnForm(request.POST)
            if form.is_valid():
                instance = form.save()
                add_notification(request.user, instance, 'Zwrot', 'Nowy zwrot został dodany')
                messages.success(request, 'Zwrot został utworzony!')
                return redirect('admin_panel')

        if 'set_day' in request.POST:
            day_date = request.POST.get('day_date')

            try:
                existing_day = Day.objects.get(day_date=day_date)
            except Day.DoesNotExist:
                existing_day = None

            form = DayForm(request.POST, instance=existing_day)

            if form.is_valid():
                day = form.save(commit=False)

                if existing_day:
                    existing_day.end_of_work_hour = day.end_of_work_hour
                    existing_day.save()
                    polish_month = MONTHS_PL.get(existing_day.day_date.month, '')[:3]
                    add_notification(request.user, existing_day, 'Godzina',
                                     f'Nowa godzina pracy na dzień {existing_day.day_date.strftime("%d")} {polish_month} {existing_day.day_date.strftime("%Y")} została ustawiona!')
                    messages.success(request, 'Godzina pracy została zaktualizowana!')
                else:
                    day.day_date = day_date
                    day.save()
                    new_day = Day.objects.get(day_date=day.day_date)
                    polish_month = MONTHS_PL.get(new_day.day_date.month, '')[:3]
                    add_notification(request.user, day, 'Godzina',
                                     f'Nowa godzina pracy na dzień {new_day.day_date.strftime("%d")} {polish_month} {new_day.day_date.strftime("%Y")} została ustawiona!')

                    messages.success(request, 'Godzina pracy została ustawiona!')

                return redirect('admin_panel')

        if 'generate_stock_items_pdf' in request.POST:
            stock_items_pdf = generate_stock_items_pdf()
            return stock_items_pdf

        if 'generate_delivery_pdf' in request.POST:
            start_date = request.POST.get('from')
            end_date = request.POST.get('to')

            delivery_pdf = generate_delivery_pdf(start_date, end_date)

            if delivery_pdf == 0:
                messages.error(request, "W wybranym przedziale nie ma dostaw")
            else:
                return delivery_pdf

    context = {
        'unread_notifications': unread_notifications,
        'current_date': current_date,
        'delivery_month_labels': delivery_month_labels,
        'delivery_month_data': delivery_month_data,
        'tasks_month_labels': tasks_month_labels,
        'tasks_month_data': tasks_month_data,
        'all_workers': all_workers,
        'workers_rating_dictionary': workers_rating_dictionary,
        'add_delivery_form': add_delivery_form,
        'add_task_form': add_task_form,
        'add_return_form': add_return_form,
        'day_form': day_form,
    }

    return render(request, 'admin_panel.html', context)


@login_required(login_url='login_user')
def notification(request):
    user = request.user
    user_rating = get_employee_rating(user)
    unread_notifications, read_notifications = get_notifications(request.user)
    users = UserProfile.objects.all()

    if request.method == 'POST':
        if 'mark_as_read' in request.POST:
            notification_id = request.POST.get('notification_id')

            notification = Notification.objects.get(id=notification_id)
            notification.read_by.add(request.user.userprofile)
            notification.save()
            return redirect('notification')

        if 'set_all_as_read' in request.POST:
            for notification in unread_notifications:
                notification.read_by.add(request.user.userprofile)
                notification.save()
            messages.success(request, 'Wszystkie powiadomienia oznaczone jako przeczytane!')
            return redirect('notification')

    context = {
        'user': user,
        'user_rating': user_rating,
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
        'users': users,
    }

    return render(request, 'notification.html', context)
