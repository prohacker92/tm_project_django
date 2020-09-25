from django import forms

class CheckForm(forms.Form):
   checkBox = forms.BooleanField(required=False, label="показать просмотренные")


class ChoiceForm(forms.Form):
   INTERVAL_CHOICES = (
      (False, "нет"),
      (1, "сутки"),
      (7, "неделю"),
      (30, "месяц"),
   )
   choice = forms.ChoiceField(choices=INTERVAL_CHOICES, label="показать просмотренные за")