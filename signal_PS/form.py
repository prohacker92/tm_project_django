from django import forms
from django.forms import SelectDateWidget

from my_app.models import Ps
from tm_project_django.clases.classes_for_view.classes_for_view import getUserPs
import datetime



"""
class SelectPsForm(forms.Form):
    def __init__(self, *args):
        self.user_name = args[1]
        super(SelectPsForm, self).__init__(*args)

        self.fields['select_list'] = forms.TypedChoiceField(label='ПС',
            choices=[(ps.name, ps.name) for ps in getUserPs(self.user_name)], coerce = str, required=False)

    select_list = forms.TypedChoiceField()
"""