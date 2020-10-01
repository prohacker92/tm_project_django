from datetime import datetime, timedelta

from django.contrib.auth.models import User, Group

from my_app.models import Sms_message, Viewed_messages, Ps

def getUserPs(username):
    #список подстанций данного пользователя
    return Ps.objects.filter(res__user__username=username).select_related('res')


def getUserMessages(username):
    #список сообщений данного пользователя
    return Sms_message.objects.filter(viewed_messages__user__username=username).select_related()


class ToolForView:

    def check_view(self, user_name, selected_interval):
        #gte
        if selected_interval != 'False':
            delta = datetime.now() - timedelta(days=int(selected_interval))
            return Viewed_messages.objects.filter(user__username=user_name, status_view=True, id_SMS__date__gte=delta)
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

    def __create_view_table_for_user(self, user, status_view, datetime):
        viw_sms_db = Viewed_messages()
        viw_sms_db.user = User.objects.get(id=user.id)
        viw_sms_db.id_SMS = Sms_message.objects.get(id=self.sms_id)
        viw_sms_db.status_view = status_view
        viw_sms_db.datetime_view = datetime
        viw_sms_db.sms_notification = False
        viw_sms_db.save()

    def create_view_tables(self, status_view=False, datetime=None):
    #создание таблиц просмотров СМС
        users = users_in_res(self.number)
        for user in users:
            self.__create_view_table_for_user(user, status_view, datetime)