# Generated by Django 3.0.3 on 2020-02-12 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200211_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='palestra_pertencente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Palestra'),
            preserve_default=False,
        ),
    ]
