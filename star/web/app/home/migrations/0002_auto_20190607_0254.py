# Generated by Django 2.2.2 on 2019-06-07 02:54

from django.db import migrations
import djongo.models.json


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='led_schedule',
            field=djongo.models.json.JSONField(default=[{'day': 0, 'periods': []}, {'day': 1, 'periods': []}, {'day': 2, 'periods': []}, {'day': 3, 'periods': []}, {'day': 4, 'periods': []}, {'day': 5, 'periods': []}, {'day': 6, 'periods': []}]),
        ),
    ]
