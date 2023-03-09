from django.shortcuts import render
from finance.models import Finance
from datetime import date
from django.db.models import Sum


def finance(request):
    finance = Finance.objects.all()
    finance_sum = finance.filter(movimento='entrada').aggregate(
        Sum('valor'))['valor__sum']
    finance_minus = finance.filter(
        movimento='saida').aggregate(Sum('valor'))['valor__sum']
    finance_total = finance_sum - finance_minus
    return render(request, 'finance.html', {'finance': finance,
                                            'finance_sum': finance_sum,
                                            'finance_minus': finance_minus,
                                            'finance_total': finance_total
                                            })


def new_entry(request):
    return render(request, 'new_entry.html')


def edit_entry(request):
    return render(request, 'edit_entry.html')


def del_entry(request):
    return render(request, 'del_entry.html')
