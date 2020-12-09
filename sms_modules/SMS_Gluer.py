from datetime import datetime
from my_app.models import Ps, SmsMessage
from my_app.service.services_for_view import ViewTables
from signal_PS.service.services_for_signals import SignalManager


def filter_ps(number):
    try:
        return Ps.objects.get(tel_number=number)
    except Ps.DoesNotExist:
        return Ps.objects.get(tel_number="111")


def save_SMS_in_db(number, text):
    sms_message_db = SmsMessage()
    sms_message_db.date = datetime.now().date()
    sms_message_db.time = datetime.now().time()
    sms_message_db.number = number
    sms_message_db.text_sms = text
    sms_message_db.ps = filter_ps(number)
    sms_message_db.save()
    # сюда функцию и в нее ID SMS
    view_tables = ViewTables(number, sms_message_db.id)
    view_tables.create_view_tables()
    parser = SignalManager(sms_message_db.ps.name, text)
    parser.run()


class SMS_Gluer():
    # Склейка СМС сообщений
    def __init__(self):
        self.dict = {} # словарь для временного хранения частей СМС
        self.key_SMS = "" # для id смс

    def set_SMS(self, number, text, udh_data=[]):
        # Склейка
        self.key_SMS = udh_data[0]
        if not self.dict:
            sms_list = []
            for i in range(udh_data[-2]):
                sms_list.append('_')
            # словарь пуст, запись в словарь
            self.dict[udh_data[0]] = sms_list
            self.dict[udh_data[0]][udh_data[-1]-1] = [udh_data[-2], udh_data[-1], number, text]

        elif self.dict.get(udh_data[0]):
            # Дописываем СМС
            self.dict[udh_data[0]][udh_data[-1]-1] = [udh_data[-2], udh_data[-1], number, text]
        else:
            # Запись новой СМС
            sms_list = []
            for i in range(udh_data[-2]):
                sms_list.append('_')
            self.dict[udh_data[0]] = sms_list
            self.dict[udh_data[0]][udh_data[-1] - 1] = [udh_data[-2], udh_data[-1], number, text]


    def save_SMS_fragments_in_db(self, udh_data=[]):
        # сохранение в бд и удаление из словаря если собранны все части
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
            save_SMS_in_db(temp_list[0][-2], "".join(text))
        else:
            print('=== Принято {1} часть СМС из {0} ===\nНомер: {2}'.format(udh_data[-2], udh_data[-1],
                                                                             self.dict[self.key_SMS][udh_data[-1]-1][-2]))




def create_sms_to_send(string):
    numbers, text = string.strip().split(';', 1)
    list_numbers = numbers.strip().split(',')
    return list_numbers, text