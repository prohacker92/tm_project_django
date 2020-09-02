from datetime import datetime

import os
import django

from tm_project_django.clases.classes_for_view.classes_for_view import View_tables

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()

from my_app.models import Ps, Sms_message



def filter_ps(number):
    try:
        return Ps.objects.get(tel_number=number)
    except Ps.DoesNotExist:
        return Ps.objects.get(tel_number="111")

def save_SMS_in_db(number,text):
    sms_message_db = Sms_message()
    sms_message_db.date = datetime.now().date()
    sms_message_db.time = datetime.now().time()
    sms_message_db.number = number
    sms_message_db.text_sms = text
    sms_message_db.ps = filter_ps(number)
    sms_message_db.save()
    # сюда функцию и в нее ID SMS
    view_tables = View_tables(number, sms_message_db.id)
    view_tables.create_view_tables()
    # сюда надо модуль парсинга СМС

class SMS_creator():
    # Склейка СМС сообщений
    def __init__(self):
        self.dict = {} # словарь для временного хранения чистей СМС
        self.key_SMS = "" # для id смс

    def set_SMS(self, number, text, udh_data=[]):
        # Склейка
        # udh_data = [] служебная строка СМС, хранить id, количество частей, номер части СМС
        self.key_SMS = udh_data[0]
        if not self.dict:
            # словарь пуст, запись в словарь
            self.dict[udh_data[0]] = [udh_data[-2], udh_data[-1], number, text]

        elif self.dict.get(udh_data[0]):
            # Дописываем СМС
            temp_text = self.dict.get(udh_data[0])[3]
            self.dict[udh_data[0]] = [udh_data[-2], udh_data[-1], number, temp_text + text]
        else:
            # Запись новой СМС
            self.dict[udh_data[0]] = [udh_data[-2], udh_data[-1], number, text]

    def save_SMS_fragments_in_db(self, udh_data=[]):
        # сохранение в бд и удаление из словаря если собранны все части
        if udh_data[-2] == udh_data[-1]:
            temp_list = self.dict.pop(self.key_SMS)
            print('==== Принято большое СМС ====\nНомер: {1}\nВремя: {0}\nСМС: {2}'.format(datetime.now(),
                                                                                      temp_list[2],
                                                                                      temp_list[3]))
            print('================================')
            print("содержимое словаря - ", self.dict)
            save_SMS_in_db(temp_list[2], temp_list[3])
        else:
            print('=== Принято {1} часть СМС из {0} ===\n Номер: {2}'.format(self.dict[self.key_SMS][0],
                                                                        self.dict[self.key_SMS][1],
                                                                        self.dict[self.key_SMS][2]))
            print("содержимое словаря - ", self.dict)
            print('================================')


