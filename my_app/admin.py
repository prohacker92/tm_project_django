from django.contrib import admin

# Register your models here.
from my_app.models import Sms_message, Ps, Viewed_messages, Profile


@admin.register(Ps)
class PsAdmin(admin.ModelAdmin):
    list_display = ("name","tel_number","res")


@admin.register(Sms_message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id',"ps","date","time","text_sms")


@admin.register(Viewed_messages)
class Viewed_messages_Admin(admin.ModelAdmin):
    list_display = ("id_SMS","user","status_view","datetime_view","sms_notification")

@admin.register(Profile)
class Profile_Admin(admin.ModelAdmin):
    list_display = ("user","notification","phone_num_for_notif")
