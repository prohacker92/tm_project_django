
class SmsRequest:

    def __init__(self, frequency_check=10):
        self.frequency_check = frequency_check
        self.number = None

    def set_sending_status(self, number):
        with open('/home/mamzin/code/tm_project_django/send_sms.txt', 'w') as out:
            out.write('{} '.format(number))

    def get_sending_status(self):
        with open('send_sms.txt') as inp:
            self.number = inp.readline().strip()
        return self.number

    def clear_file(self):
        f = open('send_sms.txt', 'w+')
        f.seek(0)
        f.close()
