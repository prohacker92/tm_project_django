from django import forms
from django.forms import SelectDateWidget

from my_app.service.services_for_view import get_user_ps
import datetime

year = datetime.date.today().year


class DateForm(forms.Form):
    start_date = forms.DateField(label='OT',
                                 widget=SelectDateWidget(years=range(year, year - 2, -1)))
    end_date = forms.DateField(label='ДО', initial=datetime.date.today,
                               widget=SelectDateWidget(years=range(year, year - 2, -1)))


class ArchiveForm(forms.Form):
    def __init__(self, *args):
        self.user_name = args[1]
        super(ArchiveForm, self).__init__(*args)

        self.fields['select_list'] = forms.MultipleChoiceField(label='ПС',
                                                               choices=[(ps.name, ps.name) for ps in get_user_ps(self.user_name)], required=False)

    select_list = forms.MultipleChoiceField()

