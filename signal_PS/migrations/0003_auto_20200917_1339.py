# Generated by Django 2.2.6 on 2020-09-17 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signal_PS', '0002_auto_20200624_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signal_type',
            name='type',
            field=models.CharField(max_length=12, primary_key=True, serialize=False),
        ),
    ]
