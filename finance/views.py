from django.shortcuts import render
from django.contrib.messages import constants
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from finance.models import Finance
from datetime import date
from django.utils import timezone
from django.db.models import Sum


def finance(request):
    finance = Finance.objects.all()
    today = timezone.now().date()
    
    finance_sum = finance.filter(movimento='entrada', data=today)
    
    return render(request, 'finance.html', {'finance': finance,
                                            'finance_sum': finance_sum,
                                            # 'finance_minus': finance_minus,
                                            # 'finance_total': finance_total
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
