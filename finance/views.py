from django.shortcuts import render, redirect       
from django.contrib.messages import constants
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from finance.models import Finance, Categoria_in, Categoria_out
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import user_passes_test, login_required
import pytz
import pandas as pd
from django.utils import timezone
import matplotlib.pyplot as plt
from io import BytesIO
import base64

br_tz = pytz.timezone('America/Sao_Paulo')
time_br = datetime.now(br_tz).time()


@user_passes_test(lambda u: u.is_superuser)
def finance(request):
    today = date.today()
    finance = Finance.objects.filter(data=today)
    total_dia = diario()[0]
    entrada_dia = diario()[1]
    saida_dia = diario()[2]
    total_sem = semanal()[0]
    entrada_sem = semanal()[1]
    saida_sem = semanal()[2]
    total_mes = mensal()[0]
    entrada_mes = mensal()[1]
    saida_mes = mensal()[2]
    total_ano = anual()[0]
    saida_ano = anual()[1]
    entrada_ano = anual()[2]
    chart = finance_chart()
    chart_ano = finance_year_chart()
    pie_mes_in = pie_chart_mes_in()
    pie_ano_in = pie_chart_ano_in()
    pie_mes_out = pie_chart_mes_out()
    pie_ano_out = pie_chart_ano_out()

    return render(request, 'finance.html', {'finance': finance,'total_dia': total_dia, 'total_sem': total_sem, 'total_mes': total_mes, 'total_ano': total_ano, 'saida_ano': saida_ano, 'entrada_ano': entrada_ano, 'entrada_dia': entrada_dia, 'saida_dia': saida_dia, 'entrada_sem': entrada_sem, 'saida_sem': saida_sem, 'entrada_mes': entrada_mes, 'saida_mes': saida_mes, 'dates':chart[0], 'entradas' : chart[1], 'saidas' : chart[2], 'months':chart_ano[0], 'entradas' : chart_ano[1], 'saidas' : chart_ano[2], 'pie_mes_in': pie_mes_in, 'pie_ano_in': pie_ano_in, 'pie_mes_out': pie_mes_out, 'pie_ano_out': pie_ano_out})


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
        categoria = Categoria_in.objects.all()
        return render(request, 'new_finance.html', {'finances': finances, 'data': data, 'categoria': categoria})

    elif request.method == "POST":
        obs = request.POST.get("inputObs")
        nome = request.POST.get("inputNome")
        data = request.POST.get("inputData")
        valor = round(float(request.POST.get("inputValor")), 2)
        movimento = 'entrada'
        tipo_pgto = request.POST.get("inputTipoPgto")
        categoria = request.POST.get("inputCategoria_in")

        finances = Finance(
            obs=obs,
            nome=nome,
            data=data,
            valor='R$ ' + str(valor),
            movimento=movimento,
            tipo_pgto=tipo_pgto,
            hora=time_br,
            categoria = categoria,
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
        categoria = Categoria_out.objects.all()
        return render(request, 'new_finance_out.html', {'finances': finances, 'data': data, 'categoria': categoria})

    elif request.method == "POST":
        obs = request.POST.get("inputObs")
        nome = request.POST.get("inputNome")
        data = request.POST.get("inputData")
        valor = round(float(request.POST.get("inputValor")), 2)
        movimento = 'saída'
        tipo_pgto = request.POST.get("inputTipoPgto")
        categoria = request.POST.get("inputCategoria_out")

        finances = Finance(
            obs=obs,
            nome=nome,
            data=data,
            valor='R$ ' + str(valor),
            movimento=movimento,
            hora=time_br,
            tipo_pgto=tipo_pgto,
            categoria=categoria,
        )
        
        finances.save()
        

        messages.add_message(request, constants.SUCCESS,
                             'Nova saída cadastrada com sucesso')
    return redirect('finance_dia')


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

def finance_chart():
    now = timezone.now()
    start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_month = (start_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    finance_data = Finance.objects.filter(data__range=[start_month, end_month])
    
    data = {}
    for finance in finance_data:
        day = finance.data.day
        valor = float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
        if finance.movimento == 'entrada':
            data[day] = data.get(day, {'entradas': 0, 'saidas': 0})
            data[day]['entradas'] += valor
        elif finance.movimento == 'saída':
            data[day] = data.get(day, {'entradas': 0, 'saidas': 0})
            data[day]['saidas'] += valor
    
    dates = [{'day': day} for day in range(1, end_month.day + 1)]
    entradas = [data.get(day, {'entradas': 0})['entradas'] for day in range(1, end_month.day + 1)]
    saidas = [data.get(day, {'saidas': 0})['saidas'] for day in range(1, end_month.day + 1)]
    
    return (dates, entradas, saidas)


def finance_year_chart():
    now = timezone.now()
    start_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_year = start_year.replace(month=12, day=31) + timedelta(days=1)
    finance_data = Finance.objects.filter(data__range=[start_year, end_year])
    
    data = {}
    for finance in finance_data:
        month = finance.data.month
        valor = float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
        if finance.movimento == 'entrada':
            data[month] = data.get(month, {'entradas': 0, 'saidas': 0})
            data[month]['entradas'] += valor
        elif finance.movimento == 'saída':
            data[month] = data.get(month, {'entradas': 0, 'saidas': 0})
            data[month]['saidas'] += valor
    
    months = [{'month': month} for month in range(1, 13)]
    entradas = [data.get(month, {'entradas': 0})['entradas'] for month in range(1, 13)]
    saidas = [data.get(month, {'saidas': 0})['saidas'] for month in range(1, 13)]
    
    return  (months, entradas, saidas)

def pie_chart_mes_in():
    today = date.today()
    month = today.month
    finances = Finance.objects.filter(data__month=month).filter(movimento='entrada')
    
    # Cria um dicionário para armazenar a soma dos gastos de cada categoria
    expenses_by_category = {}
    for finance in finances:
        category = finance.categoria
        if category in expenses_by_category:
            expenses_by_category[category] += float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
        else:
            expenses_by_category[category] = float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
    
    # Cria uma lista com as categorias e outra com os valores correspondentes
    categories = list(expenses_by_category.keys())
    values = list(expenses_by_category.values())
    
    # Cria um gráfico de pizza
    plt.figure(figsize=(8,6))
    plt.pie(values, labels=categories, autopct='%1.1f%%')
    plt.title(f'Entadas por categoria - Mês {month}')
    plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1.0))
    
    # Converte o gráfico em uma imagem
    from io import StringIO
    import base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def pie_chart_ano_in():
    today = date.today()
    year = today.year
    finances = Finance.objects.filter(data__year=year).filter(movimento='entrada')
    
    # Cria um dicionário para armazenar a soma dos gastos de cada categoria
    expenses_by_category = {}
    for finance in finances:
        category = finance.categoria
        if category in expenses_by_category:
            expenses_by_category[category] += float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
        else:
            expenses_by_category[category] = float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
    
    # Cria uma lista com as categorias e outra com os valores correspondentes
    categories = list(expenses_by_category.keys())
    values = list(expenses_by_category.values())
    
    # Cria um gráfico de pizza
    plt.figure(figsize=(8,6))
    plt.pie(values, labels=categories, autopct='%1.1f%%')
    plt.title(f'Entadas por categoria - Ano {year}')
    plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1.0))
    
    # Converte o gráfico em uma imagem
    from io import StringIO
    import base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def pie_chart_mes_out():
    today = date.today()
    month = today.month
    finances = Finance.objects.filter(data__month=month).filter(movimento='saída')
    
    # Cria um dicionário para armazenar a soma dos gastos de cada categoria
    expenses_by_category = {}
    for finance in finances:
        category = finance.categoria
        if category in expenses_by_category:
            expenses_by_category[category] += float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
        else:
            expenses_by_category[category] = float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
    
    # Cria uma lista com as categorias e outra com os valores correspondentes
    categories = list(expenses_by_category.keys())
    values = list(expenses_by_category.values())
    
    # Cria um gráfico de pizza
    plt.figure(figsize=(8,6))
    plt.pie(values, labels=categories, autopct='%1.1f%%')
    plt.title(f'Gastos por categoria - Mês {month}')
    plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1.0))
    
    # Converte o gráfico em uma imagem
    from io import StringIO
    import base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def pie_chart_ano_out():
    today = date.today()
    year = today.year
    finances = Finance.objects.filter(data__year=year).filter(movimento='saída')
    
    # Cria um dicionário para armazenar a soma dos gastos de cada categoria
    expenses_by_category = {}
    for finance in finances:
        category = finance.categoria
        if category in expenses_by_category:
            expenses_by_category[category] += float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
        else:
            expenses_by_category[category] = float(finance.valor.replace(',', '.').replace('R$','').replace(' ','')) if finance.valor else 0
    
    # Cria uma lista com as categorias e outra com os valores correspondentes
    categories = list(expenses_by_category.keys())
    values = list(expenses_by_category.values())
    fig, ax = plt.subplots()
    
    # Cria um gráfico de pizza
    
    plt.figure(figsize=(8,6))
    plt.pie(values, labels=categories, autopct='%1.1f%%')
    plt.title(f'Gastos por categoria - Ano {year}')
    plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1.0))
    
    
    
    # Converte o gráfico em uma imagem
    from io import StringIO
    import base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic