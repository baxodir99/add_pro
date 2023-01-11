from django import forms
from .models import *

class BusinessForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Business
        exclude = ("user",)


class OutcomeForm(forms.ModelForm):
    salary = forms.IntegerField(required=True)
    marketing = forms.IntegerField(required=True)

    class Meta:
        model = Outcome
        exclude = ("business", "month",)
    
        # def __init__ (self, salary, marketing, *args, **kwargs):
        #     self.salary = salary
        #     self.marketing = marketing
        #     super (OutcomeForm, self).__init__ (*args, **kwargs)


class IncomeForm(forms.ModelForm):
    income = forms.IntegerField(required=True)
    customer_count = forms.IntegerField(required=True)

    class Meta:
        model = Income
        exclude = ("business", "month",)

        # def __init__ (self, income, customer_count, *args, **kwargs):
        #     self.income = income
        #     self.customer_count = customer_count
        #     super (IncomeForm, self).__init__ (*args, **kwargs)