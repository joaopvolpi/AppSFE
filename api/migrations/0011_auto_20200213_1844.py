# Generated by Django 3.0.3 on 2020-02-13 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200213_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palestra',
            name='data',
            field=models.CharField(max_length=20),
        ),
    ]
