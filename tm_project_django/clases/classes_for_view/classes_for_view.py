from django.contrib.auth.models import User, Group

from my_app.models import Sms_message, Viewed_messages, Ps



def getUserPs(username):
    #список подстанций данного пользователя
    return Ps.objects.filter(res__user__username=username).select_related('res')


def getUserMessages(username):
    #список сообщений данного пользователя
    return Sms_message.objects.filter(viewed_messages__user__username=username).select_related()


class ToolForView:

    def check_view(self, user_name, show_viwed_sms):

        if show_viwed_sms == "true":
            return Viewed_messages.objects.filter(user__username=user_name, status_view=True)
        else:
            return Viewed_messages.objects.filter(user__username=user_name, status_view=False)

def filter_ps(number):
    try:
        return Ps.objects.get(tel_number=number)
    except Ps.DoesNotExist:
        return Ps.objects.get(tel_number="111")


def users_in_res(number, notification=None):
    ps = filter_ps(number)
    res = ps.res.name
    if notification is None:
        return User.objects.filter(groups__name=res)
    elif notification is True:
        users = User.objects.filter(groups__name=res).select_related('profile')
        return users.filter(profile__notification=notification)
    else:
        return User.objects.filter(groups__name=res)

class View_tables():

    def __init__(self, tel_number_ps, sms_id):
        self.number = tel_number_ps
        self.sms_id = sms_id

    def __create_view_table_for_user(self, user):
        viw_sms_db = Viewed_messages()
        viw_sms_db.user = User.objects.get(id=user.id)
        viw_sms_db.id_SMS = Sms_message.objects.get(id=self.sms_id)
        viw_sms_db.status_view = False
        viw_sms_db.save()


    def create_view_tables(self):
    #создание таблиц просмотров СМС
        users = users_in_res(self.number)
        for user in users:
            self.__create_view_table_for_user(user)