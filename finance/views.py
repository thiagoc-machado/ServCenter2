from django.shortcuts import render
from django.contrib.messages import constants
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from finance.models import Finance
from django.db.models import Sum
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import pytz
from openpyxl import Workbook
import pandas as pd

br_tz = pytz.timezone('America/Sao_Paulo')
time_br = datetime.now(br_tz).time()


@user_passes_test(lambda u: u.is_superuser)
def finance(request):
    total_dia = diario()[0]
    total_sem = semanal()[0]
    total_mes = mensal()[0]
    total_ano = anual()[0]

    return render(request, 'finance.html', {'total_dia': total_dia, 'total_sem': total_sem, 'total_mes': total_mes, 'total_ano': total_ano})


@login_required
def finance_dia(request):
    today = date.today()
    finance = Finance.objects.filter(data=today)
    qtd = finance.count()
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data=today):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_min -= valor

    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return render(request, 'finance_dia.html', {'finance': finance,
                                                'finance_sum': finance_sum,
                                                'finance_minus': finance_minus,
                                                'finance_total': finance_total,
                                                'qtd': qtd
                                                })


@user_passes_test(lambda u: u.is_superuser)
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
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return render(request, 'finance_sem.html', {'finance': finance,
                                                'finance_sum': finance_sum,
                                                'finance_minus': finance_minus,
                                                'finance_total': finance_total,
                                                })


@user_passes_test(lambda u: u.is_superuser)
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
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return render(request, 'finance_mes.html', {'finance': finance,
                                                'finance_sum': finance_sum,
                                                'finance_minus': finance_minus,
                                                'finance_total': finance_total,
                                                })


@user_passes_test(lambda u: u.is_superuser)
def finance_ano(request):
    year = date.today().year
    finance = Finance.objects.filter(data__year=year)

    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__year=year):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return render(request, 'finance_ano.html', {'finance': finance,
                                                'finance_sum': finance_sum,
                                                'finance_minus': finance_minus,
                                                'finance_total': finance_total,
                                                })


@user_passes_test(lambda u: u.is_superuser)
def finance_tot(request):
    finance = Finance.objects.all()

    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.all():
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return render(request, 'finance_tot.html', {'finance': finance,
                                                'finance_sum': finance_sum,
                                                'finance_minus': finance_minus,
                                                'finance_total': finance_total,
                                                })


@login_required
def new_finance(request):
    if request.method == "GET":
        data = date.today().strftime('%Y-%m-%d')
        finances = Finance.objects.all()
        return render(request, 'new_finance.html', {'finances': finances, 'data': data})

    elif request.method == "POST":
        obs = request.POST.get("inputObs")
        nome = request.POST.get("inputNome")
        data = request.POST.get("inputData")
        valor = round(float(request.POST.get("inputValor")), 2)
        movimento = 'entrada'
        tipo_pgto = request.POST.get("inputTipoPgto")
        categoria_in = request.POST.get("inputCategoria_in")

        finances = Finance(
            obs=obs,
            nome=nome,
            data=data,
            valor='R$ ' + str(valor),
            movimento=movimento,
            tipo_pgto=tipo_pgto,
            hora=time_br,
            categoria_in=categoria_in,
        )
        finances.save()
        messages.add_message(request, constants.SUCCESS,
                             'Nova entrada cadastrada com sucesso')
    return redirect('finance_dia')


@login_required
def new_finance_out(request):
    if request.method == "GET":
        data = date.today().strftime('%Y-%m-%d')
        finances = Finance.objects.all()
        return render(request, 'new_finance_out.html', {'finances': finances, 'data': data})

    elif request.method == "POST":
        obs = request.POST.get("inputObs")
        nome = request.POST.get("inputNome")
        data = request.POST.get("inputData")
        valor = round(float(request.POST.get("inputValor")), 2)
        movimento = 'saída'
        tipo_pgto = request.POST.get("inputTipoPgto")

        finances = Finance(
            obs=obs,
            nome=nome,
            data=data,
            valor='R$ ' + str(valor),
            movimento=movimento,
            hora=time_br,
            tipo_pgto=tipo_pgto,
        )
        finances.save()
        messages.add_message(request, constants.SUCCESS,
                             'Nova saída cadastrada com sucesso')
    return redirect('finance')


@login_required
def edit_finance(request, id):

    if request.method == 'GET':
        return render(request, 'edit_finance.html', {
            'id': Finance.objects.get(id=id).id,
            'obs': Finance.objects.get(id=id).obs,
            'nome': Finance.objects.get(id=id).nome,
            'data': Finance.objects.get(id=id).data.strftime('%Y-%m-%d'),
            'valor': Finance.objects.get(id=id).valor,
            'movimento': Finance.objects.get(id=id).movimento,
            'tipo_pgto': Finance.objects.get(id=id).tipo_pgto,
        })

    elif request.method == "POST":
        finances = Finance.objects.get(id=id)
        finances.obs = request.POST.get("inputObs")
        finances.nome = request.POST.get("inputNome")
        finances.data = request.POST.get("inputData")
        finances.valor = request.POST.get("inputValor")
        finances.movimento = request.POST.get("in_out")
        finances.tipo_pgto = request.POST.get("inputTipoPgto")

        if finances.movimento == 'on':
            finances.movimento = "entrada"
        else:
            finances.movimento = "saída"

        finances.save()
        messages.add_message(request, constants.SUCCESS,
                             'Entrada avulsa atualizada com sucesso')
        return redirect('finance')
    else:
        return HttpResponseBadRequest('Invalid request method')


@user_passes_test(lambda u: u.is_superuser)
def del_finance(request, id):
    finances = Finance.objects.get(id=id)
    finances.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Lançamento no caixa apagado com sucesso')
    return redirect('finance')


@user_passes_test(lambda u: u.is_superuser)
def finance_xlrx(request, id):
    today = datetime.now().date()
    if id == 1:
        finance = Finance.objects.filter(data=today)
        print('dia')
    elif id == 2:
        start_of_week = today - timedelta(days=today.weekday())
        finance = Finance.objects.filter(data__gte=start_of_week)
        print('semana')
    elif id == 3:
        start_of_month = today.replace(day=1)
        finance = Finance.objects.filter(data__gte=start_of_month)
        print('mês')
    elif id == 4:
        year = date.today().year
        finance = Finance.objects.filter(data__year=year)
        print('ano')
    else:
        finance = Finance.objects.all()
        print('todos')

    # Converter os dados para um DataFrame do Pandas
    df = pd.DataFrame(list(finance.values()))

    # Configurar o nome do arquivo de download
    filename = 'workorders.xlsx'

    # Configurar o tipo de resposta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Gerar o arquivo Excel usando o Pandas e salvar no objeto HttpResponse
    df.to_excel(response, index=False)

    return response


def diario():
    today = date.today()
    finance = Finance.objects.filter(data=today)
    qtd = finance.count()
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data=today):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_min -= valor

    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)
    return (finance_total, finance_minus, finance_sum, qtd)


def semanal():
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())

    finance = Finance.objects.filter(data__gte=start_of_week)
    qtd = finance.count()
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__gte=start_of_week):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return (finance_total, finance_minus, finance_sum, qtd)


def mensal():
    today = date.today()
    start_of_month = today.replace(day=1)

    finance = Finance.objects.filter(data__gte=start_of_month)
    qtd = finance.count()
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__gte=start_of_month):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)
    return (finance_total, finance_minus, finance_sum, qtd)


def anual():
    year = date.today().year
    finance = Finance.objects.filter(data__year=year)
    qtd = finance.count()
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__year=year):
        if finances.movimento == 'entrada':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)
    return (finance_total, finance_minus, finance_sum, qtd)
