# Generated by Django 4.2.4 on 2023-10-19 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0027_comment_model_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='model_object_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='model_name',
            field=models.CharField(max_length=100),
        ),
    ]