from django.contrib import admin
from my_app.models import SmsMessage, Ps, ViewedMessages, Profile


@admin.register(Ps)
class PsAdmin(admin.ModelAdmin):
    list_display = ("name", "tel_number", "res")


@admin.register(SmsMessage)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', "ps", "date", "time", "text_sms")


@admin.register(ViewedMessages)
class ViewedMessagesAdmin(admin.ModelAdmin):
    list_display = ("id_SMS", "user", "status_view", "datetime_view", "sms_notification")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "notification", "phone_num_for_notif")
