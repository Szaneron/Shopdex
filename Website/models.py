import datetime

from django.db import models
from django.contrib.auth.models import User


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
    - status (CharField): Status of the task, choices: "Do zrobienia" or "Zrobione".
    - assigned_to (ForeignKey): User profile to whom the task is assigned.
    - is_important (BooleanField): Indicates if the task is important.
    - date (DateField): Date of the task.
    - creation_time (TimeField): Time of task creation.

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
    date = models.DateField()
    creation_time = models.TimeField(default=datetime.time)

    def __str__(self):
        return f"{self.name} - {self.date}"


class Delivery(models.Model):
    """
    Model representing delivery information.

    Fields:
    - delivery_company (CharField): Name of the delivery company, choices: "InPost", "DPD", "GLS", "Poczta", "DHL", "Media Expert".
    - form (CharField): Form of the delivery, choices: "Paczka", "Paleta".
    - quantity (IntegerField): Quantity of items.
    - description (TextField): Description of the delivery.
    - status (CharField): Status of the delivery, choices: "W drodze", "Odebrana", "Nie dostarczona".
    - date (DateField): Date of the delivery.
    - creation_time (TimeField): Time when the delivery was created.

    Methods:
    - __str__: Returns the string representation of the delivery.

    """

    DELIVERY_COMPANY_CHOICES = [
        ('InPost', 'InPost'),
        ('DPD', 'DPD'),
        ('GLS', 'GLS'),
        ('Poczta', 'Poczta'),
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
    date = models.DateField()
    creation_time = models.TimeField(default=datetime.time)

    def __str__(self):
        return f"{self.delivery_company} - {self.date}"
