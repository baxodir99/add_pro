import math
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .helpers import get_current_date
from django.db.models import Q
from django.contrib import messages
from .forms import *

from .models import *
from apps.authentication.models import *

def index(request):
    if request.user.is_authenticated and request.user.is_superuser == False:
        return render(
            request,
            'index.html',
            context={
                'data':[
                        {   
                            'business':business,
                    } for business in Business.objects.filter(user=request.user)
                ]
            })
    else:
        return render(request, 'home.html')

def vc_index(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        business = Business.objects.all()
        context = {
                'data':[
                    {
                    'user':business.user,
                    'business':business,
                    'time':Income.objects.filter(business=business).last().created_at,
                    'income':Income.objects.filter(business=business).last().income,
                    'income_foiz': round(100-(100*Income.objects.filter(business=business).last().income)/Income.objects.filter(business=business)[(len(Income.objects.filter(business=business))-2) if len(Income.objects.filter(business=business))>=2 else 0].income, 2),
                    'customer_count':Income.objects.filter(business=business).last().customer_count,
                    'customer_count_foiz':round(100-(100*Income.objects.filter(business=business).last().customer_count)/Income.objects.filter(business=business)[(len(Income.objects.filter(business=business))-2) if len(Income.objects.filter(business=business))>=2 else 0].customer_count, 2),
                    'salary':Outcome.objects.filter(business=business).last().salary,
                    'salary_foiz': round(100-100*Outcome.objects.filter(business=business).last().salary/Outcome.objects.filter(business=business)[(len(Outcome.objects.filter(business=business))-2) if len(Outcome.objects.filter(business=business))>=2 else 0].salary, 2),
                    'marketing':Outcome.objects.filter(business=business).last().marketing,
                    'marketing_foiz': round(100-100*Outcome.objects.filter(business=business).last().marketing/Outcome.objects.filter(business=business)[(len(Outcome.objects.filter(business=business))-2) if len(Outcome.objects.filter(business=business))>=2 else 0].marketing, 2)
                } for business in business
            ]}
        return render(request, 'vc_index.html', context=context)
    else:
        return render(request, 'home.html')


def business_create(request):
    if request.user.is_authenticated and request.user.is_superuser == False:
        if request.method == "POST":
            form = BusinessForm(request.POST)
            if form.is_valid():
                business = form.save(commit=False)
                business.user = request.user
                business.save()
                return redirect("index")
        form = BusinessForm()
        return render(request=request, template_name="add.html", context={"businessform":form})
    else:
        return render(request, 'home.html')

      
def report_detail(request, id):
    business = Business.objects.get(id=id)
    if request.user.is_authenticated and request.user==business.user or request.user.is_superuser == True:
        income  = Income.objects.filter(business=business)
        outcome = Outcome.objects.filter(business=business)
        context = {
            'business':business,
            'income': [{
            'income_index': 2*i+1,
            'income': income[i].income,
            'customer_count_index': 2*(i+1),
            'customer_count': income[i].customer_count,
            'created_at': income[i].created_at,
            } for i in range(0, len(income))],
            'outcome': [{
            'salary_index': 2*i+1,
            'salary': outcome[i].salary,
            'marketing_index': 2*(i+1),
            'marketing': outcome[i].marketing,
            'created_at': outcome[i].created_at,
            } for i in range(0, len(outcome))],
        }
        return render(request,'report_detail.html',context=context)
    else:
        return render(request, 'home.html')


def outcome_create(request, *args, **kwargs):
    business = f"{request.path}"
    if request.user.is_authenticated and request.user.is_superuser == False:
        date = get_current_date()
        month = int(date[5:7])
        if request.method == "POST":
            form = OutcomeForm(request.POST)
            if form.is_valid():
                business = get_object_or_404(Business, id=business[15:-16])
                outcome = form.save(commit=False)
                outcome.business = business
                outcome.month = month
                outcome.save()
                rets = f"/report_detail/{business.id}/"
                return redirect(rets)
        form = OutcomeForm()
        return render(request=request, template_name="expense_add.html", context={"outcomeform":form})
    else:
        return render(request, 'home.html')


def income_create(request, *args, **kwargs):
    business = f"{request.path}"
    if request.user.is_authenticated and request.user.is_superuser == False:
        date = get_current_date()
        month = int(date[5:7])
        if request.method == "POST":
            form = IncomeForm(request.POST)
            if form.is_valid():
                business = get_object_or_404(Business, id=business[15:-15])
                income = form.save(commit=False)
                income.business = business
                income.month = month
                income.save()
                rets = f"/report_detail/{business.id}/"
                return redirect(rets)
        form = IncomeForm()
        return render(request=request, template_name="revenue_add.html", context={"incomeform":form})
    else:
        return render(request, 'home.html')