from django.db import models
from my_app.models import Ps


class SignalType(models.Model):
    type = models.CharField('тип', max_length=12, unique=True)
    inversion = models.BooleanField("инверсия")

    def __str__(self):
        return self.type


class Voltage(models.Model):
    # заменить на поле выбора<!!!>
    value = models.CharField('напряжение', max_length=10, primary_key=True)

    class Meta:
        verbose_name_plural = 'Напряжение'


class SignalStatus(models.Model):
    status = models.CharField(max_length=30, unique=True)
    boolean_status = models.BooleanField()

    def __str__(self):
        return self.status


class Signal(models.Model):
    type = models.ForeignKey(SignalType, on_delete=models.CASCADE, verbose_name='тип')
    voltage = models.ForeignKey(Voltage, null=True, blank=True,
                                on_delete=models.SET_NULL, verbose_name="напряжение")
    name = models.CharField('наименование', max_length=50, blank=True)
    status = models.ForeignKey(SignalStatus, on_delete=models.CASCADE, verbose_name="статус")
    ps = models.ForeignKey(Ps, on_delete=models.CASCADE, verbose_name="пс")
    date_up = models.DateTimeField("обновлено")

    class Meta:
        verbose_name_plural = 'Сигналы'
        unique_together = ('type', 'voltage', 'name', 'ps')

    def __str__(self):
        return "id-{}".format(self.id)
# ----------------------------------------------------------------------------------------------


class ControllerType(models.Model):
    type = models.CharField(max_length=50, primary_key=True)


class Provider(models.Model):
    name = models.CharField(max_length=20, primary_key=True)


class SimCardNumber(models.Model):
    number = models.CharField(max_length=50, primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)


class GsmController(models.Model):
    serial_number = models.CharField(max_length=50)
    type = models.ForeignKey(ControllerType, on_delete=models.CASCADE)
    add_description = models.TextField()
    number_SIM = models.ForeignKey(SimCardNumber, on_delete=models.CASCADE)
    ps = models.ForeignKey(Ps, on_delete=models.CASCADE)

