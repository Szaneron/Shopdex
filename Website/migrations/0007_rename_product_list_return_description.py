# Generated by Django 4.2.4 on 2023-09-11 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0006_alter_return_notes_alter_return_notice_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='return',
            old_name='product_list',
            new_name='description',
        ),
    ]
