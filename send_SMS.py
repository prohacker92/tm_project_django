from __future__ import print_function
from time import sleep
import logging

PORT = '/dev/ttyUSB0'
SPEED = 115200
PIN = None

from gsmmodem.modem import GsmModem

def main():
    print('Initializing modem...')
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, SPEED )
    modem.smsTextMode = False
    modem.connect(PIN)

    try:
        #number_request = '+79370288075'
        number_request = '+79179812832'
        #number_request = '+79272294597'
        message = "Привет"
        status = modem.sendSms(number_request, message, waitForDeliveryReport=False, deliveryTimeout=20, sendFlash=False)
        print("Сообщение отправленно - " + number_request)
        print("ждем отчет")
        sleep(15)
        print(status.status)
    finally:
        modem.close();

if __name__ == '__main__':
    main()
