from __future__ import print_function
from time import sleep
from threading import Thread

from gsmmodem import GsmModem, exceptions

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()

from sms_modules.SMS_Gluer import create_sms_to_send
from sms_modules.notifications import Manager_notifications
from sms_modules.handleSMS import handleSms
from sms_modules.sms_request import SmsRequest


class Read_SMS():
    def __init__(self, PORT='/dev/ttyUSB0', SPEED=115200, PIN=None):
        #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        self.modem = GsmModem(PORT, SPEED)
        self.modem.smsTextMode = False
        self.modem.connect(PIN)
        print('Initializing modem...')

    def read_sms(self):
        # считывает сообщения из памяти (me,sm,mt,) и удаляет прочитанные
        try:
            for sms in self.modem.listStoredSms(memory='me', delete=True):
                handleSms(sms)
        except exceptions.TimeoutException as err:
            print("modem slow", err)
            sleep(5)
            return

    def send_sms(self, number='+79179812832', message="TEST"):
        # отправка сообщений. ДОБАВИТЬ ОТЧЕТ О ДОСТАВКЕ
        self.modem.sendSms(number, message)

    def modem_close(self):
        self.modem.close()
        print("модем отключен")

thrd_stop = False
def start_manager_notif(worker):
    v = Manager_notifications(viewing_time=1)
    while not thrd_stop:
        v.run_manager(worker)

global str_sms
str_sms = []
worker = Read_SMS()
thrd = Thread(target=start_manager_notif, args=(str_sms,))
thrd.start()

sms_request = SmsRequest()

try:
    while thrd.is_alive():
        number_for_send = sms_request.get_send_status()
        try:
            worker.read_sms()
        except UnicodeEncodeError as err:
            print(err)
            sleep(1)
            continue
        if str_sms:
            for t in str_sms:
                numbers, text = create_sms_to_send(t)
                for number in numbers:
                    worker.send_sms(number=number, message=text)
                    print(f"sms rev {worker.modem._smsRef-1}")
            str_sms.clear()
        if number_for_send:
            message = "/00000 INS OUTS"
            worker.send_sms(number=number_for_send, message=message)
            print(f"sms rev {worker.modem._smsRef-1} - {message} на номер {number_for_send} ")
            sms_request.clear_file()
        sleep(1)

finally:
    thrd_stop = True
    thrd.join()
    worker.modem_close()





