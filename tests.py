from time import sleep
# import logging
from datetime import datetime, timedelta
from django.utils import timezone
from time import sleep
from threading import Thread
import os
import django
from django.core.exceptions import MultipleObjectsReturned

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()
from signal_PS import models
from signal_PS.models import Signal, Signal_status
from tm_project_django.clases.classes_for_view.classes_for_view import View_tables
from my_app.models import Sms_message, Ps, Viewed_messages, Profile
from django.contrib.auth.models import Group, User
from tm_project_django.clases.sms_modules.notifications import Manager_notifications

smsps = "10:11\r\nАварийный_сигнал ОТКЛЮЧЕН\r\nПредупред_сигнал ОТКЛЮЧЕН\r\nДверь ЗАКРЫТА\r\nКЗ_35кВ_Т_1 ВКЛЮЧЕН\r\n" \
        "В_10кВ_Т_1 ОТКЛЮЧЕН\r\nПитание_БПЗ ОТКЛЮЧЕНО\r\nТН_10кВ НОРМА\r\nВ_10кВ_Ф.2 ОТКЛЮЧЕН\r\n" \
        "В_10кВ_Ф.3 ОТКЛЮЧЕН\r\nВ_10кВ_Ф.3 ВКЛЮЧЕН\r\nВ_10кВ_Ф.4 ВКЛЮЧЕН"


class SignalManager:

    def __init__(self, name_ps, text_sms):
        self.sms_signals = text_sms.split('\r\n')
        self.ps_signals = Signal.objects.filter(ps__name=name_ps)
        self.all_statuses = Signal_status.objects.all()
        self.type = None
        self.voltage = None
        self.name = None
        self.status = None
        self.datetime = datetime.now()

    def to_clear_values(self):
        self.type = None
        self.voltage = None
        self.name = None
        self.status = None

    def find_type(self, signal):
        set_types = set()
        for ps_signal in self.ps_signals:
            set_types.add(ps_signal.type.type)
        for signal_type in set_types:
            if signal.startswith(signal_type):  # переделать, взять из базы список
                self.type = signal_type


    def find_voltage(self, signal):
        set_values = set()
        for ps_signal in self.ps_signals:
            try:
                set_values.add(ps_signal.voltage.value)
            except AttributeError:
                continue
        for value in set_values:
            if value in signal:
                self.voltage = value


    def find_name(self, signal):
        set_names = set()
        for ps_signal in self.ps_signals:
            if ps_signal.name:
                try:
                    set_names.add(ps_signal.name)
                except AttributeError:
                    continue
        for name in set_names:
            if name in signal:
                self.name = name

    def find_status(self, signal):
        for status in self.all_statuses:
            if status.status in signal:
                self.status = status.status


    def change_status(self, signal):
        #Обновление статуса
        def save_status_in_bd(obj_db):
            try:
                obj_db.status = self.all_statuses.get(status=self.status)
                obj_db.date_up = timezone.now()
                obj_db.save(update_fields=["status", "date_up"])
                print("Обновлен сигнал -", end=' ')
            except Signal_status.DoesNotExist:
                print(f"не найден статус {self.status}")

        if self.type and self.voltage and self.name:
                try:
                    signal_in_db = self.ps_signals.get(type__type=self.type, voltage__value=self.voltage,
                                                       name=self.name)
                    save_status_in_bd(signal_in_db)
                    print(f"тип {self.type} напряжение {self.voltage} наименование {self.name} статус {self.status}")
                    return
                except Signal.DoesNotExist:
                    print(f"не удалось сохранить сигнал типа {self.type} напряжение {self.voltage}"
                          f" наименование {self.name} статус {self.status}")
                    return

        elif self.type and self.voltage:
                try:
                    #print('tut')
                    signal_in_db = self.ps_signals.get(type__type=self.type, voltage__value=self.voltage)
                    save_status_in_bd(signal_in_db)
                    print(f"тип {self.type} напряжение {self.voltage}  статус {self.status}")
                    return
                except Signal.DoesNotExist:
                    print(f'не удалось сохранить сигнал типа {self.type} напряжение {self.voltage} статус {self.status}')
                    return

        elif self.type and self.name:
            try:
                signal_in_db = self.ps_signals.get(type__type=self.type, name=self.name)
                save_status_in_bd(signal_in_db)
                print(f"тип {self.type}  наименование {self.name} статус {self.status}")
                return
            except Signal.DoesNotExist:
                print(f'не удалось сохранить сигнал типа {self.type} наименование {self.name} статус {self.status}')
                return
        elif self.type:
            try:
                signal_in_db = self.ps_signals.get(type__type=self.type)
                save_status_in_bd(signal_in_db)
                print(f"тип {self.type} статус {self.status}")
                return
            except Signal.DoesNotExist:
                print(f'не удалось сохранить сигнал типа {self.type} наименование {self.name} статус {self.status}')
                return

        else:
            print(f"сигнал {signal} не сохранен")

    def run(self):

        #print(self.sms_signals)
        for signal in self.sms_signals:
            try:
                signal = signal.strip().strip(" !")
                self.find_type(signal)
                self.find_voltage(signal)
                self.find_name(signal)
                self.find_status(signal)
                self.change_status(signal)
                self.to_clear_values()
            except BaseException as err:
                self.to_clear_values()
                print(err)
                continue


# _______________________________________________________________________________________________________________
"""
def sms_tester():
    text1 = "test1"
    text2 = "test2"
    text3 = "test3"
    udn1 = [1, 3, 1]
    udn2 = [1, 3, 2]
    udn3 = [1, 3, 3]

    sms_test = SMS_creator()
    sms_test.set_SMS('111', text1, udn1)
    sms_test.save_SMS_fragments_in_db(udn1)
    sms_test.set_SMS('111', text2, udn2)
    sms_test.save_SMS_fragments_in_db(udn2)
    sms_test.set_SMS('111', text3, udn3)
    sms_test.save_SMS_fragments_in_db(udn3)

#sms_tester()
"""
#pars = SignalManager("ПС 35кВ Шаховская", smsps)
#pars.run()

