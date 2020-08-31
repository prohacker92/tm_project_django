# Generated by Django 2.2.6 on 2020-02-10 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gsm_controller',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('serial_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ps',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tel_number', models.CharField(max_length=12)),
                ('controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.Gsm_controller')),
            ],
        ),
        migrations.CreateModel(
            name='Res',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sms_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=12)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('text_sms', models.TextField()),
                ('ps', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.Ps')),
            ],
        ),
        migrations.AddField(
            model_name='ps',
            name='res',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.Res'),
        ),
    ]
