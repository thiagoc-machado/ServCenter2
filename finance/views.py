from django.shortcuts import render
from django.contrib.messages import constants
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from finance.models import Finance
from django.db.models import Sum
from django.utils import timezone
from datetime import date, datetime, timedelta

def finance(request):
    finance = Finance.objects.all()
    finance_date = Finance.objects.all().order_by('data').first()
    if finance_date is not None:
        finance_date = finance_date.data
    
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.all():
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_sum += valor
        elif  finances.movimento == 'saida':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1   
    finance_total = finance_sum - finance_minus
    finance_date = ''
    latest_finance = Finance.objects.all().order_by('data').last()
    if latest_finance:
        finance_date = latest_finance.data.strftime('%d/%m/%Y')
    
    return render(request, 'finance.html', {'finance': finance,
                                            'finance_sum': finance_sum,
                                            'finance_minus': finance_minus,
                                            'finance_total': finance_total,
                                            'finance_date': finance_date
                                            })
    
def finance_dia(request):
    today = date.today()
    finance = Finance.objects.filter(data=today)
    
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data=today):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_sum += valor
        elif  finances.movimento == 'saida':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_min -= valor
                
    finance_minus = finance_min * -1   
    finance_total = finance_sum - finance_minus
    
    return render(request, 'finance_dia.html', {'finance': finance,
                                            'finance_sum': finance_sum,
                                            'finance_minus': finance_minus,
                                            'finance_total': finance_total,
                                            })


def finance_sem(request):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())

    finance = Finance.objects.filter(data__gte=start_of_week)
    
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__gte=start_of_week):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_sum += valor
        elif  finances.movimento == 'saida':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1   
    finance_total = finance_sum - finance_minus
    
    return render(request, 'finance_sem.html', {'finance': finance,
                                            'finance_sum': finance_sum,
                                            'finance_minus': finance_minus,
                                            'finance_total': finance_total,
                                            })
    
def finance_mes(request):
    today = date.today()
    start_of_month = today.replace(day=1)

    finance = Finance.objects.filter(data__gte=start_of_month)

    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__gte=start_of_month):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_sum += valor
        elif  finances.movimento == 'saida':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1   
    finance_total = finance_sum - finance_minus
    
    return render(request, 'finance_mes.html', {'finance': finance,
                                            'finance_sum': finance_sum,
                                            'finance_minus': finance_minus,
                                            'finance_total': finance_total,
                                            })
    
def finance_ano(request):
    year = date.today().year
    finance = Finance.objects.filter(data__year=year)
    
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__year=year):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_sum += valor
        elif  finances.movimento == 'saida':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1   
    finance_total = finance_sum - finance_minus
    
    return render(request, 'finance_ano.html', {'finance': finance,
                                            'finance_sum': finance_sum,
                                            'finance_minus': finance_minus,
                                            'finance_total': finance_total,
                                            })
    
def finance_tot(request):
    finance = Finance.objects.all()
    
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.all():
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_sum += valor
        elif  finances.movimento == 'saida':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1   
    finance_total = finance_sum - finance_minus
    
    return render(request, 'finance_tot.html', {'finance': finance,
                                            'finance_sum': finance_sum,
                                            'finance_minus': finance_minus,
                                            'finance_total': finance_total,
                                            })

def new_finance(request):
    if request.method == "GET":
        data = date.today().strftime('%Y-%m-%d')
        finances = Finance.objects.all()
        return render(request, 'new_finance.html', {'finances': finances, 'data': data})

    elif request.method == "POST":
        obs = request.POST.get("inputObs")
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
        data = date.today().strftime('%Y-%m-%d')
        finances = Finance.objects.all()
        return render(request, 'new_finance_out.html', {'finances': finances, 'data': data})

    elif request.method == "POST":
        obs = request.POST.get("inputObs")
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


def edit_finance(request, id):

    if request.method == 'GET':
        return render(request, 'edit_finance.html', {
            'id': Finance.objects.get(id=id).id, 
            'obs': Finance.objects.get(id=id).obs,
            'nome': Finance.objects.get(id=id).nome,
            'data': Finance.objects.get(id=id).data.strftime('%Y-%m-%d'),
            'valor': Finance.objects.get(id=id).valor,
            'movimento': Finance.objects.get(id=id).movimento,
        })

    elif request.method == "POST":
        finances = Finance.objects.get(id=id)
        finances.obs = request.POST.get("inputObs")
        finances.nome = request.POST.get("inputNome")
        finances.data = request.POST.get("inputData")
        finances.valor = request.POST.get("inputValor")
        finances.movimento = request.POST.get("in_out")
        
        if finances.movimento == 'on':
            finances.movimento = "Entrada"
        else:
            finances.movimento = "Saída"

        finances.save()
        messages.add_message(request, constants.SUCCESS,
                                 'Entrada avulsa atualizada com sucesso')
        return redirect('finance')
    else:
        return HttpResponseBadRequest('Invalid request method')


def del_finance(request, id):
    finances = Finance.objects.get(id=id)
    finances.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Lançamento no caixa apagado com sucesso')
    return redirect('finance')
