from __future__ import print_function

import logging

PORT = 'COM10'
SPEED = 9600
PIN = None

from gsmmodem.modem import GsmModem

def main():
    print('Initializing modem...')
    modem = GsmModem(PORT, SPEED )
    modem.smsTextMode = False
    modem.connect(PIN)

    try:
        number_request = '+79372219943'
        #number_request = '+79179812832'
        #number_request = '+79272294597'
        message= "/00000 INS OUTS"
        modem.sendSms(number_request, message)
        #modem.status()
    finally:
        modem.close();

if __name__ == '__main__':
    main()
