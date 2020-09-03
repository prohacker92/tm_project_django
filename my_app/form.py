from django import forms

class CheckForm(forms.Form):
   checkBox = forms.NullBooleanField(required=False, label="показать просмотренные")