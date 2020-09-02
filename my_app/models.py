from django.db import models
from django.contrib.auth.models import User, Group


#python manage.py makemigrations
#python manage.py migrate
#python manage.py migrate --fake-initial




#class Res(models.Model):
#    name = models.CharField(max_length=20, primary_key=True)

class Ps(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    tel_number = models.CharField(max_length=12)
    res = models.ForeignKey(Group, on_delete=models.CASCADE)


class Sms_message(models.Model):
    number = models.CharField(max_length=12)
    date = models.DateField()
    time = models.TimeField()
    text_sms = models.TextField()
    ps = models.ForeignKey(Ps, on_delete=models.CASCADE)

class Viewed_messages(models.Model):
    id_SMS = models.ForeignKey(Sms_message, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_view = models.NullBooleanField()
    datetime_view = models.DateTimeField(null=True, blank=True)
    sms_notification = models.NullBooleanField(null=True, blank=True)




#-----------------Тесты---------------------------------

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notification = models.NullBooleanField()
    phone_num_for_notif = models.CharField(max_length=150)
