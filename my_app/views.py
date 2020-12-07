
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from my_app.service.services_for_view import add_sms_to_wived, check_view
from my_app.form import ChoiceForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    choice = ChoiceForm()
    try:
        selected_interval = request.session['choice_status']
    except KeyError:
        selected_interval = request.session['choice_status'] = 'False'
    if request.POST:
        selected_interval = request.session['choice_status'] = request.POST['choice']
    user_name = request.user.username
    time_zone = " (МСК)"
    messages = check_view(user_name, selected_interval)

    data = {"messages": messages, "username": user_name, "time_zone": time_zone, 'choiceForm': choice}
    return render(request, "index.html", context=data)


@login_required
def table(request):
    # обновление таблицы с смс через AJAX
    user_name = request.user.username
    time_zone = " (МСК)"
    selected_interval = request.session['choice_status']

    messages = check_view(user_name, selected_interval)

    data = {"messages": messages, "username": user_name, "time_zone": time_zone}
    return render(request, "table.html", context=data)


@login_required
def view_sms(request, id):
    # отметка о просмотре смс
    bool = add_sms_to_wived(request.user.username, id)
    if bool:
        return HttpResponseRedirect("/")
    else:
        return HttpResponseNotFound("<h2>Message not found</h2>")
