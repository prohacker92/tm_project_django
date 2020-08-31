from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from signal_PS.models import Signal, Gsm_controller
from tm_project_django.clases.classes_for_view.classes_for_view import getUserPs


@login_required
def views_select_ps(request):
    listPS = getUserPs(request.user.username)


    return render(request, "selectPS.html", {'listPS': listPS})


@login_required
def views_ps(request,name):
    signals = Signal.objects.filter(ps=name)
    controllersGSM = Gsm_controller.objects.filter(ps=name)


    data = {"signals": signals, "controllersGSM": controllersGSM}
    return render(request, "PS.html", context=data)
