from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound

from tm_project_django.clases.classes_for_view.classes_for_view import ToolForView
from my_app.form import ChoiceForm
from .models import Viewed_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def index(request):
    toolView = ToolForView()
    choice = ChoiceForm()
    try:
        selected_interval = request.session['choice_status']
    except KeyError:
        selected_interval = 'False'
    if request.POST:
        selected_interval = request.session['choice_status'] = request.POST['choice']
    user_name = request.user.username
    time_zone = " (МСК)"
    messages = toolView.check_view(user_name, selected_interval)

    data = {"messages": messages, "username": user_name, "time_zone": time_zone, 'choiceForm': choice,}
    return render(request, "index.html", context=data)

@login_required
def table(request):
    toolView = ToolForView()
    user_name = request.user.username
    time_zone = " (МСК)"
    selected_interval = request.session['choice_status']

    messages = toolView.check_view(user_name, selected_interval)

    data = {"messages": messages, "username": user_name, "time_zone": time_zone}
    return render(request, "table.html", context=data)


@login_required
def view_sms(request, id):
    try:
        user = User.objects.get(username=request.user.username)
        v_message = Viewed_messages.objects.get(user=user,id=id)
        v_message.status_view = True
        v_message.datetime_view = datetime.now()
        v_message.save(update_fields=["status_view","datetime_view"])
        return HttpResponseRedirect("/")
    except v_message.DoesNotExist:
        return HttpResponseNotFound("<h2>Message not found</h2>")
