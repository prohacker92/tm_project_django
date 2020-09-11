from time import sleep
#import logging
from datetime import datetime, timedelta
from time import sleep
from threading import Thread
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm_project_django.settings')
django.setup()

from tm_project_django.clases.classes_for_view.classes_for_view import View_tables
from my_app.models import Sms_message, Ps, Viewed_messages, Profile
from django.contrib.auth.models import Group, User

now = datetime.now()
#print(now)
two_days = timedelta(2)
in_two_days = now + two_days
#print(in_two_days)

class Period_of_time:
    def __init__(self):
        self.now = datetime.now()
        self.day = timedelta(1)
        self.week = timedelta(7)
        self.mount = timedelta(30)

    def get_day(self):
        return self.now - self.day

    def get_week(self):
        return self.now - self.week

    def get_mount(self):
        return self.now - self.mount





