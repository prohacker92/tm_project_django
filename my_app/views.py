from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound

from tm_project_django.clases.classes_for_view.classes_for_view import ToolForView
from my_app.form import CheckForm
from .models import Sms_message, Viewed_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


SHOW_VIEWED_CONTENT = False# переделать эту ебетину. скорее всего в виде словаря(user:check)

@login_required
def index(request):
    toolView = ToolForView()
    checkForm = CheckForm()
    if request.POST:
        global SHOW_VIEWED_CONTENT
        SHOW_VIEWED_CONTENT = request.POST['checkBox']

    user_name = request.user.username
    time_zone = " (МСК)"
    #messages, v_mess = toolView.check_view(user_name, SHOW_VIEWED_CONTENT)
    messages = toolView.check_view(user_name, SHOW_VIEWED_CONTENT)

    data = {"messages": messages, "username": user_name, "time_zone": time_zone, 'checkForm':checkForm,}
    return render(request, "index.html", context=data)

@login_required
def table(request):
    toolView = ToolForView()
    user_name = request.user.username
    time_zone = " (МСК)"

    messages = toolView.check_view(user_name, SHOW_VIEWED_CONTENT)

    data = {"messages": messages, "username": user_name, "time_zone": time_zone}
    return render(request,"table.html", context=data)


@login_required
def view_sms(request, id):
    try:
        user = User.objects.get(username=request.user.username)
        v_message = Viewed_messages.objects.get(user=user,id=id)
        v_message.status_view = True
        v_message.save(update_fields=["status_view"])
        return HttpResponseRedirect("/")
    except v_message.DoesNotExist:
        return HttpResponseNotFound("<h2>Message not found</h2>")
