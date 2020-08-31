# Generated by Django 2.2.6 on 2020-05-09 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('my_app', '0004_viewed_messages_id_sms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signal_status',
            fields=[
                ('status', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Signal_type',
            fields=[
                ('type', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Voltage',
            fields=[
                ('value', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ps', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.Ps')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signal_PS.Signal_status')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signal_PS.Signal_type')),
                ('voltage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='signal_PS.Voltage')),
            ],
        ),
    ]
