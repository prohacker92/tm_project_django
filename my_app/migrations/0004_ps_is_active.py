# Generated by Django 2.2.6 on 2020-11-02 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_auto_20200925_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='ps',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
