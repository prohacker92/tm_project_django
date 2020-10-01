from __future__ import print_function
from time import sleep
from gsmmodem.modem import GsmModem
from datetime import datetime
import logging

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()
from my_app.models import Sms_message,Ps


def filter_ps(number):
    try:
        return Ps.objects.get(tel_number=number)
    except Ps.DoesNotExist:
        return Ps.objects.get(tel_number="111")


class Read_SMS():
    def __init__(self, PORT='ttyUSB0', SPEED=9600, PIN=None):
        self.modem = GsmModem(PORT, SPEED)
        self.modem.smsTextMode = False
        self.modem.connect(PIN)
        print('Initializing modem...')

    def read_sms(self):
        sms_message_db = Sms_message()
        for sms in self.modem.listStoredSms(memory='sm', delete=True):
            print(sms.number, sms.time, sms.text)
            sms_message_db.date = datetime.now().date()
            sms_message_db.time = datetime.now().time()
            sms_message_db.number = sms.number
            sms_message_db.text_sms = sms.text
            sms_message_db.ps = filter_ps(sms.number)
            sms_message_db.save()

            #print(sms_message_db.get())


    def modem_close(self):
        self.modem.close()
        print("модем отключен")


def run():
    sms = Read_SMS()
    i = 1
    try:
        while i == 1:
            sms.read_sms()
            #i = 2
            sleep(2)
    finally:
        sms.modem_close()

run()

#10:05 АВАРИЙНЫЙ_СИГНАЛ ОТКЛЮЧЕН ПРЕДУПРЕД_СИГН ОТКЛЮЧЕН ДВЕРЬ З
