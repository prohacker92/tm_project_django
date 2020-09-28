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
from tm_project_django.clases.classes_for_view.classes_for_view import View_tables

def edit_in_models():
    # определить статус всех сообщений(просмотренно\нет)
    for viw in Viewed_messages.objects.all():
        viw.status_view = True
        viw.save(update_fields=["status_view"])
        print("tabl - " + viw.id)

def from_bd_to_file_group():
    #all group to file
    with open('file_groups_bd.txt', 'w') as out:
        for group in Group.objects.all():
            out.write('{}\n'.format(group.name))

def from_file_to_db_group():
    # из файла в базу group
    with open('file_groups_bd.txt') as inp:
        for i in inp.readlines():
            name = i.strip('\n')
            group = Group()
            group.name = name
            group.save()
            print(f"add {name}")

def from_bd_to_file_ps():
    # все подстанции из базы в файл
    with open('file_ps_bd.txt', 'w') as out:
        for ps in Ps.objects.all():
            out.write('{}:{}:{}\n'.format(ps.name, ps.tel_number, ps.res.name))

def from_bd_to_file_sms():
    # все сообщения из базы в файл
    with open('file_sms_bd.txt', 'w') as out:
        for sms in Sms_message.objects.all():
            out.write('{}&{}&{}&{}&{}\n'.format(sms.number, sms.date, sms.time, sms.text_sms, sms.ps.name))

def from_file_to_db_ps():
    # из файла в базу подстанции
    with open('file_ps_bd.txt') as inp:
        for i in inp.readlines():
            name, tel_number, res_name = i.strip('\n').split(':')
            print(f"{name} {tel_number} {res_name}")
            ps = Ps()
            ps.name = name
            ps.tel_number = tel_number
            ps.res = Group.objects.get(name=res_name)
            ps.save()
            print(f"add {name}")

def from_file_to_database_sms():
    # из файла в базу sms
    string = ''
    with open('file_sms_bd.txt') as inp:
        for i in inp.readlines():
            string += i
    string = string.replace('\n', " ").split('#')
    for s in string:
        if s:
            print(s)
            split_str = s.split('&')
            number = split_str[0].strip()
            print(number)
            date = split_str[1].strip()
            print(date)
            time = split_str[2].strip()
            print(time)
            text_sms = split_str[3].strip()
            print(text_sms)
            ps_name = split_str[4].strip()
            print(ps_name)
            print(number, date, time, text_sms, ps_name)
            sms = Sms_message()
            sms.number = number
            sms.date = date
            sms.time = time
            sms.text_sms = text_sms
            sms.ps = Ps.objects.get(name=ps_name)
            sms.save()



def tablview_for_allusers():
    #создание таблиц просмотра для всех пользователей
    for sms in Sms_message.objects.all():
        tab_viw = View_tables(sms.number, sms.id)
        tab_viw.create_view_tables(status_view=True, datetime=datetime.combine(sms.date, sms.time))
        print(sms.id)

#tablview_for_allusers()
#edit_in_models()
#from_bd_to_file_ps()
#from_file_to_db_ps()
#from_file_to_database_sms()
#from_bd_to_file_sms()
#from_bd_to_file_group()
#from_file_to_db_group()

#for group in Group.objects.all():
#    print(group.name.strip('\n'))