from django.contrib.auth.models import User, Group

from my_app.models import Sms_message, Viewed_messages, Ps



def getUserPs(username):
    if username == "admin":
        return Ps.objects.all()

    elif username == "ODS":
        return Ps.objects.all().exclude(name="ТЕСТ ПС1").exclude(name="не зарегистрирован")
    else:
        group = Group.objects.get(user__username=username)
        return Ps.objects.filter(res=group)


def getUserMessages(user_name):
    #переписать. оптимизировать запрос
    messages = None
    if user_name == "admin":
        messages = Sms_message.objects.all()

    elif user_name == "ODS":
        messages = Sms_message.objects.all().exclude(ps="ТЕСТ ПС1").exclude(ps="не зарегистрирован")
        print(user_name)
    else:
        for g in Group.objects.all():
            for u in User.objects.filter(groups__name=g.name):
                if user_name == u.username:
                    print(g.name)
                    messages = Sms_message.objects.filter(ps__res=g.name)

    return messages


class ToolForView:

    def check_view(self, user_name, SHOW_VIEWED_CONTENT):

        #v_messages = Viewed_messages.objects.filter(user__username=user_name)
        if SHOW_VIEWED_CONTENT == "true":
            print(SHOW_VIEWED_CONTENT)
            print(Viewed_messages.objects.filter(user__username=user_name, status_view=True))
            return Viewed_messages.objects.filter(user__username=user_name, status_view=True)
        else:
            print(SHOW_VIEWED_CONTENT)
            print(Viewed_messages.objects.filter(user__username=user_name, status_view=False))
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

        users = users_in_res(self.number )
        for user in users:
            self.__create_view_table_for_user(user)