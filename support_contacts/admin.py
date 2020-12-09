from django.contrib import admin

from support_contacts.models import SupportСontacts


@admin.register(SupportСontacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("position","name","email","numbers")