# Generated by Django 3.0.3 on 2020-03-02 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20200302_2000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='palestra',
            old_name='descricaopalestra',
            new_name='descricao_palestra',
        ),
        migrations.RenameField(
            model_name='palestra',
            old_name='descricaopalestrante',
            new_name='descricao_palestrante',
        ),
        migrations.RenameField(
            model_name='palestra',
            old_name='fotopalestrante',
            new_name='foto_palestrante',
        ),
    ]
