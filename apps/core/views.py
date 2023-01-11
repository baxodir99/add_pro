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
    date = get_current_date()
    month = int(date[5:7])
    
    if request.user.is_authenticated and request.user.is_superuser == True:
        business = Business.objects.all()
        context = {
                'data':[
                    {
                    'user':business.user,
                    'business':business,
                    'income':Income.objects.filter(Q(business=business) & Q(month=month)).values_list('income', flat=True).first(),
                    'customer_count':Income.objects.filter(Q(business=business) & Q(month=month)).values_list('customer_count', flat=True).first(),
                    'salary':Outcome.objects.filter(Q(business=business) & Q(month=month)).values_list('salary', flat=True).first(),
                    'marketing':Outcome.objects.filter(Q(business=business) & Q(month=month)).values_list('marketing', flat=True).first(),
                    'month':month,
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
        context = {
            'business':business,
            'income': [{
            'income': income.income,
            'customer_count': income.customer_count,
            'month': income.month
            } for income in Income.objects.filter(business=business)],
            'outcome': [{
            'salary': outcome.salary,
            'marketing': outcome.marketing,
            'month': outcome.month
            } for outcome in Outcome.objects.filter(business=business)],
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
                outcome = Outcome.objects.filter(Q(month=month) & Q(business=business[15:-16]))
                if outcome:
                    messages.info(request, "expense already created this month.") 
                    rets = f"/report_detail/{outcome[0].business.id}/"
                    return redirect(rets)
                else:
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
                income = Income.objects.filter(Q(month=month) & Q(business=business[15:-15]))
                if income:
                    messages.info(request, "expense already created this month.")
                    rets = f"/report_detail/{income[0].business.id}/"
                    return redirect(rets)
                else:
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