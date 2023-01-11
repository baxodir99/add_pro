from django import forms
from .models import *

class BusinessForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Business
        exclude = ("user",)


class OutcomeForm(forms.ModelForm):
    salary = forms.IntegerField(required=True, min_value=0)
    marketing = forms.IntegerField(required=True, min_value=0)

    class Meta:
        model = Outcome
        exclude = ("business", "month",)

class IncomeForm(forms.ModelForm):
    income = forms.IntegerField(required=True, min_value=0)
    customer_count = forms.IntegerField(required=True, min_value=0)

    class Meta:
        model = Income
        exclude = ("business", "month",)