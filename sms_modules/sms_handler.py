from __future__ import print_function
import logging
from time import sleep

from gsmmodem import exceptions
from gsmmodem.modem import GsmModem
from .SMS_Gluer import SMS_Gluer, save_SMS_in_db

message = SMS_Gluer()


def sms_handle(sms):
    try:
        if sms.udh:
            message.set_SMS(sms.number, sms.text, sms.udh[0].data)

            for i in sms.udh:
                # print("id = ", i.id)
                # print("dataLength = ", i.dataLength)
                print("data = ", i.data)
            message.save_SMS_fragments_in_db(sms.udh[0].data)
        else:
            print(
                '============= Принято короткое СМС =============\nНомер: {0}\nВремя: {1}\nСМС: {2}'.format(sms.number,
                                                                                                            sms.time,
                                                                                                            sms.text))
            save_SMS_in_db(sms.number, sms.text)
            print('=' * 50)

    except AttributeError:
        print(
            f"reference {sms.reference} timeSent {sms.timeSent} timeFinalized {sms.timeFinalized}"
            f" deliveryStatus {sms.deliveryStatus}")
        return


class MyGsmModem(GsmModem):

    def read_sms(self):
        # считывает сообщения из памяти (me,sm,mt,) и удаляет прочитанные
        try:
            for sms in self.listStoredSms(memory='me', delete=True):
                #sms_handle(sms)
                print(sms.text)
        except exceptions.TimeoutException as err:
            print("modem slow", err)
            sleep(5)
            return

    def send_sms(self, number='+79179812832', message="TEST"):
        # отправка сообщений. ДОБАВИТЬ ОТЧЕТ О ДОСТАВКЕ
        self.sendSms(number, message)

    def modem_close(self):
        self.close()
        print("модем отключен")





"""
    def __init__(self, PORT='/dev/ttyUSB0', SPEED=115200, PIN=None):
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        self.modem = GsmModem(PORT, SPEED, smsReceivedCallbackFunc=handleSms)
        self.modem.smsTextMode = False
        self.modem.connect(PIN)
        print('Initializing modem...')

    def run(self):
        print('Waiting for SMS message...')
        try:
            self.modem.rxThread.join(9999999)
        finally:
            self.modem.close()
"""