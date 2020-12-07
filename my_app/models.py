from django.db import models
from django.contrib.auth.models import User, Group


class Ps(models.Model):
    name = models.CharField('Наименование', max_length=100, primary_key=True)
    tel_number = models.CharField("Номер СИМ", max_length=12)
    res = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="РЭС")
    is_active = models.BooleanField("В сети")

    class Meta:
        verbose_name_plural = "Подстанции"

    def __str__(self):
        return self.name


class SmsMessage(models.Model):
    number = models.CharField('Номер', max_length=12)
    date = models.DateField("Дата")
    time = models.TimeField("Время")
    text_sms = models.TextField("Текст сообщения")
    ps = models.ForeignKey(Ps, on_delete=models.CASCADE, verbose_name="ПС")

    class Meta:
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return "{} - {} - {}".format(self.date, self.time, self.ps)


class ViewedMessages(models.Model):
    id_SMS = models.ForeignKey(SmsMessage, on_delete=models.CASCADE, verbose_name='СМС')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    status_view = models.BooleanField("Просмотрено")
    datetime_view = models.DateTimeField("Дата просмотра", blank=True)
    sms_notification = models.BooleanField("СМС уведомление")

    class Meta:
        verbose_name_plural = "Квитирование"

    def __str__(self):
        return "{} - {}".format(self.id_SMS, self.user)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    notification = models.BooleanField("уведомление")
    phone_num_for_notif = models.CharField("номера для оповещения", max_length=150,
                                           help_text="вводить через запятую")

    class Meta:
        verbose_name_plural = "Расширение профилей"
