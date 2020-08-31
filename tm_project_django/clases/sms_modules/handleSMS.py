from __future__ import print_function

import logging
from gsmmodem.modem import GsmModem
from tm_project_django.clases.sms_modules.SMS_creator import SMS_creator, save_SMS_in_db


message = SMS_creator()

def handleSms(sms):

    if sms.udh:
      message.set_SMS(sms.number, sms.text, sms.udh[0].data)
      #message.set_SMS(sms)

      for i in sms.udh:
        print("id = ", i.id)
        print("dataLength = ", i.dataLength)
        print("dataLength = ", i.data)
      message.save_SMS_fragments_in_db(sms.udh[0].data)
    else:
        print('===== Принято короткое СМС =====\nНомер: {0}\nВремя: {1}\nСМС: {2}'.format(sms.number, sms.time, sms.text))
        save_SMS_in_db(sms.number, sms.text)
        print('================================')

class HandleSMS():

    def __init__(self, PORT = '/dev/ttyUSB0', SPEED = 115200, PIN = None):
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        self.modem = GsmModem(PORT, SPEED, smsReceivedCallbackFunc = handleSms)
        self.modem.smsTextMode = False
        self.modem.connect(PIN)
        print('Initializing modem...')

    def run(self):
        print('Waiting for SMS message...')
        try:
            self.modem.rxThread.join(9999999)
        finally:
            self.modem.close()
