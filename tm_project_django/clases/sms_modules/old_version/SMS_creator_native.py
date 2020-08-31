
class SMS_creator2():
    def __init__(self):
        self.dict = {}
        self.key_SMS = ""

    def set_SMS(self, number, text, udh_data=[]):
        self.key_SMS = udh_data[0]
        if not self.dict:
            print("словарь пуст, запись в словарь")
            self.dict[udh_data[0]] = [udh_data[1], udh_data[2], number, text]

        elif self.dict.get(udh_data[0]):
            temp_text = self.dict.get(udh_data[0])[3]
            print("Дописываем СМС")
            self.dict[udh_data[0]] = [udh_data[1], udh_data[2], number, temp_text + text]
        else:
            print("Запись новой СМС")
            self.dict[udh_data[0]] = [udh_data[1], udh_data[2], number, text]

    def save_to_SMS_db(self, udh_data=[]):
        if udh_data[1] == udh_data[2]:
            temp_list = self.dict.pop(self.key_SMS)
            print("конечное СМС = ", temp_list[2] + temp_list[3])
            print("содержимое словаря - ", self.dict)
        else:
            print("СМС = ", self.dict[self.key_SMS])