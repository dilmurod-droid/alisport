# Generated by Django 5.0.7 on 2024-07-24 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='every_or_one',
            field=models.CharField(choices=[('everyday', 'Every-Day'), ('in_one_day', 'In-one-day')], default='in_one_day', max_length=10),
        ),
    ]
