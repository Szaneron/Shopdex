# Generated by Django 4.2.4 on 2023-10-19 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0026_task_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='model_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]