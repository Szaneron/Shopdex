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

        Methods:
        - __str__: Returns the string representation of the user profile.

        """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    assigned_tasks = models.PositiveIntegerField(default=0)
    completed_tasks = models.PositiveIntegerField(default=0)

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
