# Generated by Django 5.1.2 on 2024-11-05 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='modified',
            new_name='last_modified',
        ),
    ]
