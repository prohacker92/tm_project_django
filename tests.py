from time import sleep
#import logging
from datetime import datetime, timedelta
from django.utils import timezone
from time import sleep
from threading import Thread
import os
import django
from django.core.exceptions import MultipleObjectsReturned

from tm_project_django.clases.sms_modules.SMS_creator import SMS_creator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()
from signal_PS import models
from signal_PS.models import Signal, Signal_status
from tm_project_django.clases.classes_for_view.classes_for_view import View_tables
from my_app.models import Sms_message, Ps, Viewed_messages, Profile
from django.contrib.auth.models import Group, User


sms = "КОНТРОЛЛЕР ВКЛЮЧЕН\n ОХРАНА ПИТ. В НОРМЕ (15,0v)\n АКБ 100% Т 42C \nВ_10кВ_Ф.2 ОТКЛЮЧЕН !\n В_10кВ_Ф.3 ОТКЛЮЧЕН !" \
      "\n ДВЕРЬ ЗАКРЫТА ! \nВ_35кВ_Т_1 ВКЛЮЧЕН !\n В_10кВ_Т_1 ОТКЛЮЧЕН !\n ТН_10кВ_N1 ЗЕМЛЯ_В_СЕТИ !" \
      "\n В_10кВ_Ф.1 ОТКЛЮЧЕН !\n Питание_БПЗ_Т_1 ОТКЛЮЧЕНО !\n АВАРИЙНЫЙ_СИГНАЛ ВКЛЮЧЕН !\n ПРЕДУПРЕД_СИГН ВКЛЮЧЕН !" \
      "\n ПИТАНИЕ ВОССТАНОВЛЕНО"

class SignalManager:

    def __init__(self, name_ps, text_sms):
        self.sms_signals = text_sms.split('\n')
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
        if signal.startswith("ДВЕРЬ"): #переделать, взять из базы список

            self.type, signal = signal.split(" ", 1)
            print("найдена ", self.type)
            return signal
        try:
            self.type, signal = signal.split("_", 1)
        except:
            print(f'не распознан тип {signal}')
            return None
        try:
            self.ps_signals.get(type__type=self.type)
            return signal
        except Signal.DoesNotExist:
            print(f' не распознан тип {self.type}')
            return None
        except MultipleObjectsReturned:
            return signal

    def find_voltage(self, signal):
        if signal.startswith("10кВ") or signal.startswith("35кВ") or signal.startswith("110кВ"): #взять из базы список напряжений
            self.voltage, signal = signal.split("_", 1)
            return True, signal
        else:
            return False, signal

    def find_name(self, signal):
        self.name, signal = signal.split(" ")
        return signal

    def find_status(self, signal):
        self.status = signal
        return signal

    def print_signal(self):

        if self.type:
            if self.voltage and self.name:
                print(f"тип {self.type} напряжение {self.voltage} наименование {self.name} статус {self.status}")
            else:
                print(f'тип {self.type} статус {self.status}')
        else:
            print("Ошибка!!!")

    def change_status(self):

        if self.type:
            if self.voltage and self.name:
                try:
                    signal_in_db = self.ps_signals.get(type__type=self.type, voltage__value=self.voltage, name=self.name)
                    signal_in_db.status = self.all_statuses.get(status=self.status)
                    signal_in_db.date_up = timezone.now()
                    signal_in_db.save(update_fields=["status", "date_up"])
                    print("Статус обновлен")
                except Signal.DoesNotExist:
                    print(f"не удалось сохранить сигнал типа {self.type} напряжение {self.voltage}"
                          f" наименование {self.name} статус {self.status}")
                except Signal_status.DoesNotExist:
                    print(f"не найден статус {self.status}")
            else:
                try:
                    signal_in_db = self.ps_signals.get(type__type=self.type)
                    signal_in_db.status = self.all_statuses.get(status=self.status)
                    signal_in_db.date_up = timezone.now()
                    signal_in_db.save(update_fields=["status", "date_up"])
                    print("Статус обновлен")
                except Signal.DoesNotExist:
                    print(f'не удалось сохранить сигнал типа {self.type} статус {self.status}')
                except Signal_status.DoesNotExist:
                    print(f"не найден статус {self.status}")
        else:
            print("Ошибка!!!")

    def run(self):

        print(self.sms_signals)
        for signal in self.sms_signals:
            #try:
                signal = signal.strip().strip(" !")
                signal = self.find_type(signal)
                if signal:
                    is_voltage, signal = self.find_voltage(signal)
                    if is_voltage:
                        signal = self.find_name(signal)
                        signal = self.find_status(signal)
                        self.print_signal()
                        self.change_status()
                        #print("остаток ", signal)
                        self.to_clear_values()
                    else:
                        signal = self.find_status(signal)
                        self.print_signal()
                        self.change_status()
                        #print("остаток ", signal)
                        self.to_clear_values()
                else:
                    continue
            #except ValueError:
            #    print(f"ошибка в парсинге {signal}")
             #   continue

#_______________________________________________________________________________________________________________
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
"""

#sms_tester()

def from_bd_to_file_group():
    #all group to file
    with open('file_groups_bd.txt', 'w') as out:
        for group in Group.objects.all():
            out.write('{}\n'.format(group.name))

from_bd_to_file_group()