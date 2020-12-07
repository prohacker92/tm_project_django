from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from archive.form import ArchiveForm, DateForm
from my_app.service.services_for_view import getUserMessages


@login_required
def show_archive(request):
    # переписать в класс!!!
    user_name = request.user.username
    archive_form = ArchiveForm(request.POST or None, user_name)
    date_form = DateForm(request.POST or None)
    messages = None
    start_date = None
    if request.POST:
        messages = getUserMessages(user_name)

        if archive_form.is_valid() and date_form.is_valid():

            if archive_form.cleaned_data.get("select_list"):
                list_ps_name = list()
                for ps_name in archive_form.cleaned_data.get("select_list"):
                    list_ps_name.append(ps_name)
                messages = messages.filter(ps__name__in=list_ps_name)

            if date_form.cleaned_data.get("start_date"):
                start_date = date_form.cleaned_data.get("start_date")

            if date_form.cleaned_data.get("end_date"):
                end_date = date_form.cleaned_data.get("end_date")
                messages = messages.filter(date__range=(start_date, end_date))

    data = {'archive_form': archive_form, 'date_form': date_form, 'messages': messages}
    return render(request, "archive.html", context=data)



