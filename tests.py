from time import sleep
#import logging
from datetime import datetime
from time import sleep
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()

from my_app.models import Sms_message, Ps, Res, Viewed_messages, Profile
from django.contrib.auth.models import Group, User


"""
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

#for ps in getUserPs("SarRes"):
   # print(ps.name)

date1 = datetime.now()
print(date1)
sleep(2)
date2 = datetime.now()
print(date2.timedelta)"""

def filter_ps(number):
    try:
        return Ps.objects.get(tel_number=number)
    except Ps.DoesNotExist:
        return Ps.objects.get(tel_number="111")

def users_in_res(number_sms):

    ps = filter_ps(number_sms)
    res = ps.res.name
    users = User.objects.filter(groups__name = res).select_related('profile')
    users = users.filter(profile__notification=True)
    return users

def create_view_tables(tel_number_ps, sms_id):
    users = users_in_res(tel_number_ps)
    for user in users:
        viw_sms_db = Viewed_messages()
        viw_sms_db.user = User.objects.get(id=user.id)
        viw_sms_db.id_SMS = Sms_message.objects.get(id=sms_id)
        viw_sms_db.status_view = False
        viw_sms_db.save()


#Users_in_res('+79179812832')
def edit_in_models():
    for viw in Viewed_messages.objects.all():
        viw.status_view = True
        viw.save(update_fields=["status_view"])

#edit_in_models()
print(Viewed_messages.objects.get(user__username="admin",id_SMS__id=516))
