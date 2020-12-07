from datetime import datetime, timedelta

from django.contrib.auth.models import User

from my_app.models import Sms_message, Viewed_messages, Ps


def add_sms_to_wived(username, id_sms):
    # отметка о просмотре смс пользователем
    try:
        #user = User.objects.get(username=username)
        v_message = Viewed_messages.objects.get(user__username=username, id=id_sms)
        v_message.status_view = True
        v_message.datetime_view = datetime.now()
        v_message.save(update_fields=["status_view", "datetime_view"])
        return True
    except v_message.DoesNotExist:
        return False


def get_user_ps(username):
    # список подстанций данного пользователя
    # добавить обратную связь в модели
    return Ps.objects.filter(res__user__username=username).select_related('res')


def get_user_messages(username):
    # список сообщений данного пользователя
    # добавить обратную связь в модели
    return Sms_message.objects.filter(viewed_messages__user__username=username).select_related()


def check_view(user_name, selected_interval):
    # показать просмотренные смс за период
    if selected_interval != 'False':
        delta = datetime.now() - timedelta(days=int(selected_interval))
        return Viewed_messages.objects.filter(user__username=user_name, status_view=True, id_SMS__date__gte=delta)
    else:
        return Viewed_messages.objects.filter(user__username=user_name, status_view=False)


def filter_ps(number):
    # смс не от пс в незарегистрированные
    try:
        return Ps.objects.get(tel_number=number)
    except Ps.DoesNotExist:
        return Ps.objects.get(tel_number="111")


def users_in_res(number, notification=None):
    ps = filter_ps(number)
    res_name = ps.res.name
    if notification:
        users = User.objects.filter(groups__name=res_name).select_related('profile')
        return users.filter(profile__notification=notification)
    else:
        return User.objects.filter(groups__name=res_name)


class ViewTables:
    # перенести сюда метод для отметки о просмотре
    def __init__(self, tel_number_ps, sms_id):
        self.number = tel_number_ps
        self.sms_id = sms_id

    def _create_view_table_for_user(self, user, status_view):
        viw_sms_db = Viewed_messages(user=User.objects.get(id=user.id),
                                     id_SMS=Sms_message.objects.get(id=self.sms_id),
                                     status_view=status_view,
                                     sms_notification=False)
        viw_sms_db.save()

    def create_view_tables(self, status_view=False):
        # создание таблиц просмотров СМС
        users = users_in_res(self.number)
        for user in users:
            self._create_view_table_for_user(user, status_view)
