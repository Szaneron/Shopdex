from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class UserProfile(models.Model):
    """
    Model representing user profiles in the application.

    Fields:
    - user (OneToOneField): One-to-one relationship with the built-in User model.
    - profile_picture (ImageField, optional): Profile picture of the user.
    - assigned_tasks (PositiveIntegerField, default=0): Number of assigned tasks.
    - completed_tasks (PositiveIntegerField, default=0): Number of completed tasks.
    - position (CharField): User's position, choices: "Pracownik" or "Szef".

    Methods:
    - __str__: Returns the string representation of the user profile.

    """

    POSITION_CHOICES = [
        ('Pracownik', 'Pracownik'),
        ('Szef', 'Szef'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    assigned_tasks = models.PositiveIntegerField(default=0)
    completed_tasks = models.PositiveIntegerField(default=0)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='Pracownik')

    def __str__(self):
        return self.user.username


class Task(models.Model):
    """
    Model representing tasks assigned to users.

    Fields:
    - name (CharField): Name of the task.
    - description (TextField): Description of the task.
    - status (CharField): Status of the task, available choices defined in STATUS_CHOICES.
    - assigned_to (ForeignKey): User profile to whom the task is assigned.
    - is_important (BooleanField): Indicates if the task is important.
    - task_date (DateField): Date of the task.
    - creation_time (DateTimeField): Date and time when the task was created.

    Methods:
    - __str__: Returns the string representation of the task.

    """

    STATUS_CHOICES = [
        ('Do zrobienia', 'Do zrobienia'),
        ('Zrobione', 'Zrobione'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='todo')
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_important = models.BooleanField(default=False)
    task_date = models.DateField(default=timezone.now)
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.task_date}"


class Delivery(models.Model):
    """
    Model representing delivery information.

    Fields:
    - delivery_company (CharField): Name of the delivery company, available choices defined in DELIVERY_COMPANY_CHOICES.
    - form (CharField): Form of the delivery, available choices defined in FORM_CHOICES.
    - quantity (IntegerField): Quantity of items.
    - description (TextField): Description of the delivery.
    - status (CharField): Status of the delivery, available choices defined in STATUS_CHOICES.
    - delivery_date (DateField): Date of the delivery.
    - creation_time (DateTimeField): Date and time when delivery task was created.

    Methods:
    - __str__: Returns the string representation of the delivery.

    """

    DELIVERY_COMPANY_CHOICES = [
        ('InPost', 'InPost'),
        ('DPD', 'DPD'),
        ('GLS', 'GLS'),
        ('Poczta', 'Poczta'),
        ('Paczkomat', 'Paczkomat'),
        ('DHL', 'DHL'),
        ('Media Expert', 'Media Expert'),
    ]

    FORM_CHOICES = [
        ('Paczka', 'Paczka'),
        ('Paleta', 'Paleta'),
    ]

    STATUS_CHOICES = [
        ('W drodze', 'W drodze'),
        ('Odebrana', 'Odebrana'),
        ('Nie dostarczona', 'Nie dostarczona'),
    ]

    delivery_company = models.CharField(max_length=15, choices=DELIVERY_COMPANY_CHOICES)
    form = models.CharField(max_length=10, choices=FORM_CHOICES, default='Paczka')
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='W drodze')
    delivery_date = models.DateField(default=timezone.now)
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.delivery_company} - {self.delivery_date}"


class Day(models.Model):
    """
    Model representing work day information.

    Fields:
    - end_of_work_hour (TimeField): The time when work ends.
    - date (DateField): The date of the work day.

    Methods:
    - __str__: Returns the string representation of the work day.

    """
    end_of_work_hour = models.TimeField()
    day_date = models.DateField(default=timezone.now, unique=True)

    def __str__(self):
        return f"{self.day_date} - {self.end_of_work_hour}"


class Return(models.Model):
    """
    Model representing return information.

    Fields:
    - name (CharField): Name of the return.
    - product_list (TextField): List of products for the return.
    - status (CharField): Status of the return, available choices defined in STATUS_CHOICES.
    - return_date (DateField): Date when the return should be prepared.
    - creation_time (DateTimeField): Date and time when the task was created.

    Methods:
    - __str__: Returns the string representation of the return.

    """
    STATUS_CHOICES = [
        ('Do spakowania', 'Do spakowania'),
        ('Przygotowany', 'Przygotowany'),
        ('Odebrany', 'Odebrany'),
    ]

    name = models.CharField(max_length=100)
    product_list = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    return_date = models.DateField(default=timezone.now)
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.return_date}"
