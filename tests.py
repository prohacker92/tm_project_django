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

notification = False

if notification is None:
    print(notification)
elif notification is True:
    print(notification)
else:
    print(notification)