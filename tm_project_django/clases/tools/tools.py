from time import sleep
#import logging
from datetime import datetime
from time import sleep
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()

from my_app.models import Sms_message, Ps, Viewed_messages, Profile
from django.contrib.auth.models import Group, User

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
    # определить статус всех сообщений(просмотренно\нет)
    for viw in Viewed_messages.objects.all():
        viw.status_view = True
        viw.save(update_fields=["status_view"])

#edit_in_models()


#with open('file_ps_bd.txt','w') as out:
    #все подстанции из базы в файл
#    for ps in Ps.objects.all():
#       out.write('{}:{}:{}\n'.format(ps.name, ps.tel_number, ps.res.name))

#with open('file_sms_bd.txt','w') as out:
    #все сообщения из базы в файл
#    for sms in Sms_message.objects.all():
#       out.write('{}:{}:{}:{}:{}\n'.format(sms.number, sms.date, sms.time, sms.text_sms, sms.ps.name))

def from_file_to_database_ps():
    # из файла в базу подстанции
    with open('file_ps_bd.txt') as inp:
        for i in inp.readlines():
            name, tel_number, res_name = i.strip('\n').split(':')
            #print(res_name)
            print(name,tel_number,res_name)
            ps = Ps()
            ps.name = name
            ps.tel_number = tel_number
            ps.res = Group.objects.get(name=res_name)
            ps.save()

#from_file_to_database()

def from_file_to_database_sms():
    # из файла в базу sms
    string = ''
    with open('file_sms_bd.txt') as inp:
        for i in inp.readlines():
            string += i
    string = string.replace('\n', " ").split('+')
    for s in string:
        if s:
            print(s)
            split_str = s.split(':')
            number = '+' + split_str[0].strip()
            print(number)
            date = split_str[1].strip()
            print(date)
            time = split_str[2] + ':' + split_str[3] + ':' + split_str[4].strip()
            print(time)
            text_sms = split_str[-3] + ':' + split_str[-2].strip()
            if ':' in text_sms:
                text_sms = text_sms.split(':')[-1]
            print (text_sms)
            ps_name = split_str[-1].strip()
            print(ps_name)
            print(number, date, time, text_sms, ps_name)
            sms = Sms_message()
            sms.number = number
            sms.date = date
            sms.time = time
            sms.text_sms = text_sms
            sms.ps = Ps.objects.get(name=ps_name)
            sms.save()

#from_file_to_database_sms()