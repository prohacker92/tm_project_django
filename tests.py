from time import sleep
#import logging
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


class SMS_creator():
    # Склейка СМС сообщений
    def __init__(self):
        self.dict = {} # словарь для временного хранения частей СМС
        self.key_SMS = "" # для id смс

    def set_SMS(self, number, text, udh_data=[]):
        # Склейка
        # udh_data = [] служебная строка СМС, хранить id, количество частей, номер части СМС
        self.key_SMS = udh_data[0]
        if not self.dict:
            sms_list = []
            for i in range(udh_data[-2]):
                sms_list.append('_')
            print(sms_list)
            print(udh_data[-1]-1)
            # словарь пуст, запись в словарь
            #self.dict[udh_data[0]] = [udh_data[-2], udh_data[-1], number, text]
            self.dict[udh_data[0]] = sms_list
            self.dict[udh_data[0]][udh_data[-1]-1] = [udh_data[-2], udh_data[-1], number, text]
            print(self.dict[udh_data[0]])

        elif self.dict.get(udh_data[0]):
            # Дописываем СМС
            #temp_text = self.dict.get(udh_data[0])[3]
            #self.dict[udh_data[0]] = [udh_data[-2], udh_data[-1], number, temp_text + text]
            self.dict[udh_data[0]][udh_data[-1]-1] = [udh_data[-2], udh_data[-1], number, text]
        else:
            # Запись новой СМС
            #self.dict[udh_data[0]] = [udh_data[-2], udh_data[-1], number, text]
            sms_list = []
            for i in range(udh_data[-2]):
                sms_list.append('_')
            self.dict[udh_data[0]] = sms_list
            self.dict[udh_data[0]][udh_data[-1] - 1] = [udh_data[-2], udh_data[-1], number, text]

    def save_SMS_fragments_in_db(self, udh_data=[]):
        # сохранение в бд и удаление из словаря если собранны все части
        #if udh_data[-2] == udh_data[-1]:
        if '_' not in self.dict[udh_data[0]]:
            temp_list = self.dict.pop(self.key_SMS)
            text = []
            for element in temp_list:
                text.append(element[-1])
            print('==== Принято большое СМС ====\nНомер: {1}\nВремя: {0}\nСМС: {2}'.format(datetime.now(),
                                                                                      temp_list[0][-2],
                                                                                      "".join(text)))
            print('================================')
            print("содержимое словаря - ", self.dict)
            #save_SMS_in_db(temp_list[0][-2], "".join(text))
        else:
            print('=== Принято {1} часть СМС из {0} ===\n Номер: {2}'.format(udh_data[-2], udh_data[-1],
                                                                             self.dict[self.key_SMS][udh_data[-1]-1][-2]))




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