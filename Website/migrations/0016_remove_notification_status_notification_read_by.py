# Generated by Django 4.2.4 on 2023-09-27 19:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Website', '0015_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='status',
        ),
        migrations.AddField(
            model_name='notification',
            name='read_by',
            field=models.ManyToManyField(related_name='read_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
