# Generated by Django 5.0.6 on 2024-06-19 19:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_userprofile_borrowed_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowedbook',
            name='borrowing_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
