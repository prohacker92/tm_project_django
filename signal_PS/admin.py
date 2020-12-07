from django.contrib import admin
from signal_PS.models import Signal


@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "voltage", "name", "status", "ps")
    list_filter = ['voltage__value', "ps__name"]
    search_fields = ['^voltage__value', "^ps__name", "name", "status__status", "type__type"]


