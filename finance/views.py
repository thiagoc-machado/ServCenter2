from django.shortcuts import render
from django.contrib.messages import constants
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
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


def new_finance(request):
    if request.method == "GET":
        data=date.today().strftime('%Y-%m-%d')
        finances = Finance.objects.all()
        return render(request, 'new_finance.html', {'finances': finances, 'data': data})
    
    elif request.method == "POST":
        obs = request.POST.get("inputOs")
        nome = request.POST.get("inputNome")
        data = request.POST.get("inputData")
        valor = request.POST.get("inputValor")
        movimento = 'entrada'
        
        finances = Finance(
            obs=obs,
            nome=nome,
            data=data,
            valor=valor,
            movimento=movimento,
            )
        finances.save()
        messages.add_message(request, constants.SUCCESS,
                                 'Nova entrada cadastrada com sucesso')
    return redirect('finance')

def new_finance_out(request):
    if request.method == "GET":
        data=date.today().strftime('%Y-%m-%d')
        finances = Finance.objects.all()
        return render(request, 'new_finance_out.html', {'finances': finances, 'data': data})
    
    elif request.method == "POST":
        obs = request.POST.get("inputOs")
        nome = request.POST.get("inputNome")
        data = request.POST.get("inputData")
        valor = request.POST.get("inputValor")
        movimento = 'saida'
        
        finances = Finance(
            obs=obs,
            nome=nome,
            data=data,
            valor=valor,
            movimento=movimento,
            )
        finances.save()
        messages.add_message(request, constants.SUCCESS,
                                 'Nova saída cadastrada com sucesso')
    return redirect('finance')


def edit_finance(request):
    return render(request, 'edit_finance.html')


def del_finance(request):
    return render(request, 'del_entry.html')
