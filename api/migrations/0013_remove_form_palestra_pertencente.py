# Generated by Django 3.0.3 on 2020-02-17 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200213_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='palestra_pertencente',
        ),
    ]
