# Generated by Django 2.2.2 on 2019-06-17 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20190617_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='ssh_pub',
            field=models.CharField(blank=True, default='ssh-rsa [key] [comment]', max_length=1000, verbose_name='SSH Public Key'),
        ),
    ]
