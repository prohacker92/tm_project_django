from django.contrib import admin

from support_contacts.models import Support_contacts


@admin.register(Support_contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("position","name","email","numbers")