# Generated by Django 3.0 on 2020-01-27 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_palestra_foto_palestrante'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='foto_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_perfil'),
        ),
    ]