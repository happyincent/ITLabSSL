# Generated by Django 2.2.1 on 2019-06-04 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20190604_1750'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historyinfo',
            old_name='pm2_5',
            new_name='pmat25',
        ),
    ]
