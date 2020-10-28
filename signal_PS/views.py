from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from my_app.service.services_for_view import getUserPs
from signal_PS.service.services_for_signals import get_signals_of_ps, get_ps_tel_number
from sms_modules.sms_request import SmsRequest

@login_required
def views_select_ps(request):
    list_models_PS = getUserPs(request.user.username)

    return render(request, "selectPS.html", {'listPS': list_models_PS})


@login_required
def views_ps(request, name_ps):
    signals = get_signals_of_ps(name_ps)
    sms_request = SmsRequest()
    status = ""
    if request.method == "POST":
        number_ps = get_ps_tel_number(name_ps)
        sms_request.set_sending_status(number_ps)
        status = ">>> отправлено"

    data = {"signals": signals, "name": name_ps, "status": status}
    return render(request, "PS.html", context=data)
