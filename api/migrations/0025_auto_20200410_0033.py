# Generated by Django 3.0.4 on 2020-04-10 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_dias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dias',
            name='pri',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='dias',
            name='qua',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='dias',
            name='qui',
            field=models.CharField(default='04-04-2020', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dias',
            name='seg',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='dias',
            name='ter',
            field=models.CharField(max_length=10),
        ),
    ]