# Generated by Django 4.2.4 on 2023-10-19 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0028_comment_model_object_name_alter_comment_model_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='model_object_name',
        ),
    ]