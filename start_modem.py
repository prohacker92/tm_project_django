from time import sleep

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()

from sms_modules.sms_handler import MyGsmModem

reader = MyGsmModem(port='/dev/ttyUSB0', baudrate=115200)

while True:
    reader.smsTextMode = False
    reader.connect(None)
    print('Initializing modem...')
    reader.read_sms()
    sleep(2)