from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from datetime import date, time
from finance.models import Finance

@login_required
def dashboard(request):
    if request.method == "GET":
        today = date.today()
        finance = Finance.objects.filter(data=today)
        qtd = finance.count()
        

        reg_hour = []
        for i in range(8, 18):
            reg_hour.append(Finance.objects.filter(data=today, hora__hour=i).values('valor'))
            
        for i in range(len(reg_hour)):
            print(reg_hour[i-1])

        
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
                                                'qtd': qtd, 'reg_hour': reg_hour
                                                })

    else:
        return HttpResponseBadRequest('Invalid request method') 