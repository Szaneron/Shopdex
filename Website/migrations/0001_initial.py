# Generated by Django 4.2.4 on 2023-08-29 21:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_of_work_hour', models.TimeField()),
                ('day_date', models.DateField(default=django.utils.timezone.now, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_company', models.CharField(choices=[('InPost', 'InPost'), ('DPD', 'DPD'), ('GLS', 'GLS'), ('Poczta', 'Poczta'), ('Paczkomat', 'Paczkomat'), ('DHL', 'DHL'), ('Media Expert', 'Media Expert')], max_length=15)),
                ('form', models.CharField(choices=[('Paczka', 'Paczka'), ('Paleta', 'Paleta')], default='Paczka', max_length=10)),
                ('quantity', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('W drodze', 'W drodze'), ('Odebrana', 'Odebrana'), ('Nie dostarczona', 'Nie dostarczona')], default='W drodze', max_length=15)),
                ('delivery_date', models.DateField(default=django.utils.timezone.now)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('product_list', models.TextField()),
                ('status', models.CharField(choices=[('Do spakowania', 'Do spakowania'), ('Przygotowany', 'Przygotowany'), ('Odebrany', 'Odebrany')], max_length=20)),
                ('return_date', models.DateField(default=django.utils.timezone.now)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures')),
                ('assigned_tasks', models.PositiveIntegerField(default=0)),
                ('completed_tasks', models.PositiveIntegerField(default=0)),
                ('position', models.CharField(choices=[('Pracownik', 'Pracownik'), ('Szef', 'Szef')], default='Pracownik', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Do zrobienia', 'Do zrobienia'), ('Zrobione', 'Zrobione')], default='todo', max_length=12)),
                ('is_important', models.BooleanField(default=False)),
                ('task_date', models.DateField(default=django.utils.timezone.now)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.userprofile')),
            ],
        ),
    ]
