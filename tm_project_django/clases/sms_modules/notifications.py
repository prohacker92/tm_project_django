from datetime import datetime, timedelta
from time import sleep

from my_app.models import Viewed_messages


class Manager_notifications():

    def __init__(self, frequency_check=10, viewing_time=60):
        self.frequency_check = frequency_check
        self.viewing_time = viewing_time


    def search_for_unseen_sms(self):
        delta = datetime.now() - timedelta(minutes=self.viewing_time)
        return Viewed_messages.objects.filter(status_view=False, sms_notification=False, user__profile__notification=True,
                                              id_SMS__time__lte=delta).exclude(id_SMS__ps__name='не зарегистрирован')


    def run_manager(self,str_sms):

        unseen_sms = self.search_for_unseen_sms()
        if unseen_sms:
            for v in unseen_sms:
                sms_messages = "{};(УОПИ сервер) ({}) {}".format(v.user.profile.phone_num_for_notif, v.id_SMS.ps.name,
                                                                 v.id_SMS.text_sms)
                str_sms.append(sms_messages)
                print("Сообщение {} отправленно от {} для {} на номерa {}".format(v.id_SMS.text_sms, v.id_SMS.ps.name,
                                                                    v.user.username, v.user.profile.phone_num_for_notif))
                v.sms_notification = True
                v.save(update_fields=["sms_notification"])
        sleep(self.frequency_check)



