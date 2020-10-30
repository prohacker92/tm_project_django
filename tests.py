# import logging
from datetime import datetime
from django.utils import timezone
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()
from signal_PS.models import Signal, Signal_status


# _______________________________________________________________________________________________________________
"""
def sms_tester():
    text1 = "test1"
    text2 = "test2"
    text3 = "test3"
    udn1 = [1, 3, 1]
    udn2 = [1, 3, 2]
    udn3 = [1, 3, 3]

    sms_test = SMS_creator()
    sms_test.set_SMS('111', text1, udn1)
    sms_test.save_SMS_fragments_in_db(udn1)
    sms_test.set_SMS('111', text2, udn2)
    sms_test.save_SMS_fragments_in_db(udn2)
    sms_test.set_SMS('111', text3, udn3)
    sms_test.save_SMS_fragments_in_db(udn3)

#sms_tester()
"""
#pars = SignalManager("ПС 35кВ Шаховская", smsps)
#pars.run()

#ps_signals = Signal.objects.filter(ps__name="ТЕСТ ПС1")
#for signal in ps_signals:
#    result = signal.type.type
#    if signal.voltage:
#        result += " " + signal.voltage.value
#    if signal.name:
#        result += " " + signal.name
#    print(result)

l = ["1", "q1","2", "sadsa", 'sas', "a","22","aslfsdkjfdskfhkdsh", 'safdsasd']
set(l)
l.sort(key=len, reverse=True)
print(l)