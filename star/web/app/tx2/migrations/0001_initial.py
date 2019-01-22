# Generated by Django 2.1.5 on 2019-01-22 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstantInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField(default=0.0)),
                ('humidity', models.FloatField(default=0.0)),
                ('pm2_5', models.FloatField(default=0.0)),
                ('loudness', models.FloatField(default=0.0)),
                ('light_intensity', models.FloatField(default=0.0)),
                ('uv_intensity', models.FloatField(default=0.0)),
                ('ir_sensed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info_now', to='home.Device')),
            ],
        ),
    ]
