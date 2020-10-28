from datetime import datetime
from time import timezone

from signal_PS.models import Signal_status, Signal
from my_app.models import Ps


def get_ps_tel_number(name_ps):
    return Ps.objects.get(name=name_ps).tel_number

def get_signals_of_ps(name_ps):
    return Signal.objects.filter(ps=name_ps)


class SignalManager:
    # парсинг смс для поиска сигналов и обновления их статуса в БД
    def __init__(self, name_ps, text_sms):
        self.sms_signals = text_sms.split('\r\n')
        self.ps_signals = Signal.objects.filter(ps__name=name_ps)
        self.all_statuses = Signal_status.objects.all()
        self.type = None
        self.voltage = None
        self.name = None
        self.status = None
        self.datetime = datetime.now()

    def to_clear_values(self):
        # очистка значений сигнала
        self.type = None
        self.voltage = None
        self.name = None
        self.status = None

    def find_type(self, signal):
        # поиск типа сигнала
        set_types = set()
        for ps_signal in self.ps_signals:
            set_types.add(ps_signal.type.type)
        for signal_type in set_types:
            if signal.startswith(signal_type):
                self.type = signal_type

    def find_voltage(self, signal):
        # поиск напряжения
        list_values = []
        for ps_signal in self.ps_signals:
            try:
                list_values.append(ps_signal.voltage.value)
            except AttributeError:
                continue
        for value in set(list_values):
            if value in signal:
                self.voltage = value

    def find_name(self, signal):

        set_names = set()
        for ps_signal in self.ps_signals:
            if ps_signal.name:
                try:
                    set_names.add(ps_signal.name)
                except AttributeError:
                    continue
        for name in set_names:
            if name in signal:
                self.name = name

    def find_status(self, signal):
        for status in self.all_statuses:
            if status.status in signal:
                self.status = status.status

    def change_status(self, signal):
        # Обновление статуса
        def save_status_in_bd(obj_db):
            try:
                obj_db.status = self.all_statuses.get(status=self.status)
                obj_db.date_up = self.datetime
                obj_db.save(update_fields=["status", "date_up"])
                print("Обновлен сигнал -", end=' ')
            except Signal_status.DoesNotExist:
                print(f"не найден статус {self.status}")

        if self.type and self.voltage and self.name:
            try:
                signal_in_db = self.ps_signals.get(type__type=self.type, voltage__value=self.voltage,
                                                   name=self.name)
                save_status_in_bd(signal_in_db)
                print(f"тип {self.type} напряжение {self.voltage} наименование {self.name} статус {self.status}")
                return
            except Signal.DoesNotExist:
                print(f"не удалось сохранить сигнал типа {self.type} напряжение {self.voltage}"
                      f" наименование {self.name} статус {self.status}")
                return

        elif self.type and self.voltage:
            try:
                # print('tut')
                signal_in_db = self.ps_signals.get(type__type=self.type, voltage__value=self.voltage)
                save_status_in_bd(signal_in_db)
                print(f"тип {self.type} напряжение {self.voltage}  статус {self.status}")
                return
            except Signal.DoesNotExist:
                print(f'не удалось сохранить сигнал типа {self.type} напряжение {self.voltage} статус {self.status}')
                return

        elif self.type and self.name:
            try:
                signal_in_db = self.ps_signals.get(type__type=self.type, name=self.name)
                save_status_in_bd(signal_in_db)
                print(f"тип {self.type}  наименование {self.name} статус {self.status}")
                return
            except Signal.DoesNotExist:
                print(f'не удалось сохранить сигнал типа {self.type} наименование {self.name} статус {self.status}')
                return
        elif self.type:
            try:
                signal_in_db = self.ps_signals.get(type__type=self.type)
                save_status_in_bd(signal_in_db)
                print(f"тип {self.type} статус {self.status}")
                return
            except Signal.DoesNotExist:
                print(f'не удалось сохранить сигнал типа {self.type} наименование {self.name} статус {self.status}')
                return

        else:
            print(f"сигнал {signal} не сохранен")

    def run(self):

        for signal in self.sms_signals:
            #try:
                signal = signal.strip().strip(" !")
                self.find_type(signal)
                self.find_voltage(signal)
                self.find_name(signal)
                self.find_status(signal)
                self.change_status(signal)
                self.to_clear_values()
            #except BaseException as err:
                #self.to_clear_values()
                #print(err)
                #continue
