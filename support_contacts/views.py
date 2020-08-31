from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from support_contacts.models import Support_contacts


@login_required
def contacts(request):
    contacts = Support_contacts.objects.all()

    data = {"contacts": contacts}

    return render(request, "contacts.html",context=data)
