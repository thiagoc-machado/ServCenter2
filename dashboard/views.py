from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from datetime import date
from datetime import datetime
from finance.models import Finance
from pytz import timezone as tz


def get_today_values():
    today = datetime.now(tz('America/Sao_Paulo')).date()
    start = tz(
        'America/Sao_Paulo').localize(datetime.combine(today, datetime.min.time()))
    end = tz(
        'America/Sao_Paulo').localize(datetime.combine(today, datetime.max.time()))
    return Finance.objects.filter(data__range=(start, end))


def get_values_by_hour():
    values = [0] * 11  # 11 horas de trabalho, das 8h às 18h
    today_values = get_today_values()
    for value in today_values:
        if value.movimento == 'entrada':
            value_datetime = datetime.combine(value.data, value.hora)
            value_datetime = tz('America/Sao_Paulo').localize(value_datetime)
            hour = value_datetime.hour - 8  # ajuste de índice da lista
            if 0 <= hour <= 10:
                value_str = value.valor.replace(
                    'R$', '').replace(',', '.').strip()
                value_float = float(value_str)
                values[hour] += value_float
    return values


def get_output_by_hour():
    values = [0] * 11  # 11 horas de trabalho, das 8h às 18h
    today_values = get_today_values()
    for value in today_values:
        if value.movimento == 'saída':
            value_datetime = datetime.combine(value.data, value.hora)
            value_datetime = tz('America/Sao_Paulo').localize(value_datetime)
            hour = value_datetime.hour - 8  # ajuste de índice da lista
            if 0 <= hour <= 10:
                value_str = value.valor.replace(
                    'R$', '').replace(',', '.').strip()
                value_float = float(value_str)
                values[hour] += value_float
    return values


@login_required
def dashboard(request):
    if request.method == "GET":
        today = date.today()

        finance = Finance.objects.filter(data=today)
        qtd = finance.count()
        values_by_hour = get_values_by_hour()
        output_by_hour = get_output_by_hour()

        finance_sum = 0
        finance_min = 0
        for finances in Finance.objects.filter(data=today):
            if finances.movimento == 'entrada':
                valor = finances.valor
                if valor is not None:
                    valor = float(valor.replace('R$', '').replace(',', '.'))
                    finance_sum += valor
            elif finances.movimento == 'saida':
                valor = finances.valor
                if valor is not None:
                    valor = float(valor.replace('R$', '').replace(',', '.'))
                    finance_min -= valor

        finance_minus = finance_min * -1
        finance_total = finance_sum - finance_minus
        return render(request, 'dashboard.html', {'finance': finance,
                                                  'finance_sum': finance_sum,
                                                  'finance_minus': finance_minus,
                                                  'finance_total': finance_total,
                                                  'qtd': qtd,
                                                  'values_by_hour': values_by_hour,
                                                  'output_by_hour': output_by_hour
                                                  })

    else:
        return HttpResponseBadRequest('Invalid request method')
