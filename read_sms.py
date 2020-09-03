from __future__ import print_function
from time import sleep
from gsmmodem.modem import GsmModem
from datetime import datetime
import logging

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()

from tm_project_django.clases.sms_modules.handleSMS import handleSms


class Read_SMS():
    def __init__(self, PORT='/dev/ttyUSB0', SPEED=115200, PIN=None):
        #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        self.modem = GsmModem(PORT, SPEED)
        self.modem.smsTextMode = False
        self.modem.connect(PIN)
        self.sms_list = []
        self.sms_status = None
        print('Initializing modem...')

    def read_sms(self):
        #считывает сообщения из памяти (me,sm,mt,) и удаляет прочитанные
        for sms in self.modem.listStoredSms(memory='me', delete=True):
            handleSms(sms)
            self.sms_list.append(sms)

    def send_sms(self, number='+79179812832', message="TEST"):
        # отправка сообщений. ДОБАВИТЬ ОТЧЕТ О ДОСТАВКЕ

        self.sms_status = self.modem.sendSms(number, message)

    def modem_close(self):
        self.modem.close()
        print("модем отключен")

def run():
    worker = Read_SMS()

    try:
        while True:

            worker.read_sms()

            sleep(1)

    finally:
        worker.modem_close()

run()
