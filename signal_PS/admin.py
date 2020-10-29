from django.contrib import admin

# Register your models here.
from signal_PS.models import Signal, Signal_type, Voltage, Signal_status, Controller_type, Provider, SIM_card_number, \
    Gsm_controller


@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "voltage", "name", "status", "ps")
    list_filter = ['voltage__value', "ps__name"]
    search_fields = ['^voltage__value', "^ps__name", "name", "status__status", "type__type"]


@admin.register(Signal_type)
class TypeSigAdmin(admin.ModelAdmin):
    list_display = ("type",)

@admin.register( Voltage)
class VoltageAdmin(admin.ModelAdmin):
    list_display = ("value",)

@admin.register(Signal_status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("status",)

#-------------------------------------------------------------

#admin.site.register(Controller_type)
#admin.site.register(Provider)
#admin.site.register(SIM_card_number)

#@admin.register(Gsm_controller)
#class ControllerGSM_Admin(admin.ModelAdmin):
 #   list_display = ("serial_number","type","number_SIM","ps")