from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from my_app.models import Ps
from signal_PS.models import Signal, Gsm_controller
from tm_project_django.clases.classes_for_view.classes_for_view import getUserPs
from tm_project_django.clases.sms_modules.sms_request import SmsRequest


@login_required
def views_select_ps(request):
    listPS = getUserPs(request.user.username)

    return render(request, "selectPS.html", {'listPS': listPS})


@login_required
def views_ps(request,name):
    signals = Signal.objects.filter(ps=name)
    controllersGSM = Gsm_controller.objects.filter(ps=name)
    sms_request = SmsRequest()
    if request.method == "POST":
        print("post")
        number_ps = Ps.objects.get(name=name).tel_number
        sms_request.set_send_status(number_ps)


    data = {"signals": signals, "controllersGSM": controllersGSM}
    return render(request, "PS.html", context=data)
