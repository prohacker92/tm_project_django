from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms

# Create your views here.
from archive.form import ArchiveForm, DateForm
from my_app.models import Ps
from tm_project_django.clases.classes_for_view.classes_for_view import getUserMessages
import datetime

@login_required
def show_archive(request):
    user_name = request.user.username
    archiveForm = ArchiveForm(request.POST or None, user_name)
    dateForm = DateForm(request.POST or None)
    messages = None
    startDate = ''
    endDate = ''
    if request.POST:
        messages = getUserMessages(user_name)

        if archiveForm.is_valid() and dateForm.is_valid():

            if archiveForm.cleaned_data.get("select_list"):
                for t in archiveForm.cleaned_data.get("select_list"):
                    ps = Ps.objects.get(name=t)
                    messages = messages.filter(ps=ps)

            if dateForm.cleaned_data.get("start_date"):
                startDate = dateForm.cleaned_data.get("start_date")

            if dateForm.cleaned_data.get("end_date"):
                endDate = dateForm.cleaned_data.get("end_date")
                messages = messages.filter(date__range=(startDate, endDate))

    data = {'archiveForm': archiveForm, 'dateForm': dateForm, 'messages': messages}
    return render(request, "archive.html", context=data)



