# Generated by Django 2.2.6 on 2020-08-31 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0008_auto_20200826_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ps',
            name='res',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
        migrations.DeleteModel(
            name='Res',
        ),
    ]