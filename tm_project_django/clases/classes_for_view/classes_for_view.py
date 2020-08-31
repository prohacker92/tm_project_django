from django.contrib.auth.models import User, Group

from my_app.models import Sms_message, Viewed_messages, Ps



def getUserPs (user_name):
    ps = None
    if user_name == "admin":
        ps = Ps.objects.all()

    elif user_name == "ODS":
        ps = Ps.objects.all().exclude(name="ТЕСТ ПС1").exclude(name="не зарегистрирован")
    else:
        for g in Group.objects.all():
            for u in User.objects.filter(groups__name=g.name):
                if user_name == u.username:
                    print(g.name)
                    ps = Ps.objects.filter(res=g.name)

    return ps


def getUserMessages(user_name):
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
    """
    def check_view(self, user_name, SHOW_VIEWED_CONTENT):
        # переименовать переменные!!!
        messages = getUserMessages(user_name)

        a = []
        b = []
        c = []
        user = User.objects.get(username=user_name)
        viewed_messages = Viewed_messages.objects.filter(user=user)
        for viw in viewed_messages:
            a.append(viw.id_SMS.id)
        for message in messages:
            if message.id not in a:
                b.append(message)
            else:
                if SHOW_VIEWED_CONTENT == "true":
                    c.append(message)

        return b, c
"""
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
        #return v_messages

        #user = User.objects.get(username=user_name)
        #viewed_messages = Viewed_messages.objects.filter(user=user)


        #return