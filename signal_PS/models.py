from django.db import models

# Create your models here.
from my_app.models import Ps

class Signal_type(models.Model):
    type = models.CharField(max_length=12, primary_key=True)
    inversion = models.BooleanField()

class Voltage(models.Model):
    value = models.CharField(max_length=10, primary_key=True)

class Signal_status(models.Model):
    status = models.CharField(max_length=30, primary_key=True)
    boolean_status = models.BooleanField()

class Signal(models.Model):
    type = models.ForeignKey(Signal_type, on_delete=models.CASCADE)
    voltage = models.ForeignKey(Voltage,null=True,blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50,blank=True)
    status = models.ForeignKey(Signal_status, on_delete=models.CASCADE)
    ps = models.ForeignKey(Ps, on_delete=models.CASCADE)
    date_up = models.DateTimeField()

"""----------------------------------------------------------------------------------------------------"""

class Controller_type(models.Model):
    type = models.CharField(max_length=50, primary_key=True)

class Provider(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

class SIM_card_number(models.Model):
    number = models.CharField(max_length=50, primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

class Gsm_controller(models.Model):
    serial_number = models.CharField(max_length=50)
    type = models.ForeignKey(Controller_type, on_delete=models.CASCADE)
    add_description = models.TextField()
    number_SIM = models.ForeignKey(SIM_card_number, on_delete=models.CASCADE)
    ps = models.ForeignKey(Ps, on_delete=models.CASCADE)

