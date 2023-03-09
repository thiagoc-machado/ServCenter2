from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Services
from .models import client
from .models import Employees
from .models import work_order as work_order_model
from finance.models import Finance


@login_required
def work_order(request):
    if request.method == "GET":
        # serv = Services.objects.all()
        workorders = work_order_model.objects.all()
        #print(Services.objects.get(cod=id).nome)
        return render(request, 'work_order.html', {'workorders': workorders})
    else:
        return HttpResponseBadRequest('Invalid request method')


@login_required
def new_work_order(request):

    if request.method == "GET":
        list_client = client.objects.all()
        list_employee = Employees.objects.all()
        list_service = Services.objects.all()
        hora = datetime.now().time()
        data = datetime.now().date().strftime("%Y-%m-%d")
        print(data)
        return render(request, 'new_work_order.html', {'list_client': list_client,
                                                       'list_employee': list_employee,
                                                       'list_service': list_service,
                                                       'data': data,
                                                       'hora': hora,
                                                       })

    elif request.method == "POST":

        list_client = client.objects.all()
        list_employee = Employees.objects.all()
        list_service = Services.objects.all()

        if request.POST.get("pgto_adiantado") == None:
            pgto_adiantado = False
        else:
            pgto_adiantado = True
        if request.POST.get("os_finalizada") == None:
            os_finalizada = False
        else:
            os_finalizada = True

        if not request.POST.get("cod_cli").isnumeric() or not request.POST.get("cod_tecnico").isnumeric() or not request.POST.get("cod_ser").isnumeric():
            messages.add_message(request, constants.ERROR,
                                 'Verifique os dados inseridos')
            return render(request, 'new_work_order.html', {
                'list_client': list_client,
                'list_employee': list_employee,
                'list_service': list_service,
                'cliente': request.POST.get("cliente"),
                'cod_cli': request.POST.get("cod_cli"),
                'cod_tecnico': request.POST.get("cod_tecnico"),
                'cod_ser': request.POST.get("cod_ser"),
                'cod_user': request.POST.get("cod_user"),
                'whatsapp': request.POST.get("whatsapp"),
                'status': request.POST.get("status"),
                'obs_cli': request.POST.get("obs_cli"),
                'produto': request.POST.get("produto"),
                'marca': request.POST.get("marca"),
                'modelo': request.POST.get("modelo"),
                'serie': request.POST.get("serie"),
                'condicao': request.POST.get("condicao"),
                'acessorios': request.POST.get("acessorios"),
                'defeito': request.POST.get("defeito"),
                'obs_ser': request.POST.get("obs_ser"),
                'solucao': request.POST.get("solucao"),
                'preco': request.POST.get("preco"),
                'desconto': request.POST.get("desconto"),
                'acressimo': request.POST.get("acressimo"),
                'total': request.POST.get("total"),
                'modo_pgto': request.POST.get("modo_pgto"),
                'pgto_adiantado': request.POST.get("pgto_adiantado"),
                'os_finalizada': request.POST.get("os_finalizada"),
                'condicao': request.POST.get("condicao"),
                'hora': datetime.now().time(),
                'data': datetime.now().date().strftime("%Y-%m-%d"),
            })

        work_orders = work_order_model(

            cod_cli=client.objects.get(pk=request.POST.get("cod_cli")),
            cod_tec=Employees.objects.get(pk=request.POST.get("cod_tecnico")),
            cod_ser=Services.objects.get(pk=request.POST.get("cod_ser")),
            cod_user=request.user,
            whatsapp=request.POST.get("whatsapp"),
            status=request.POST.get("status"),
            obs_cli=request.POST.get("obs_cli"),
            produto=request.POST.get("produto"),
            marca=request.POST.get("marca"),
            modelo=request.POST.get("modelo"),
            serie=request.POST.get("serie"),
            condicao=request.POST.get("condicao"),
            acessorios=request.POST.get("acessorios"),
            defeito=request.POST.get("defeito"),
            obs_ser=request.POST.get("obs_ser"),
            solucao=request.POST.get("solucao"),
            preco=request.POST.get("preco"),
            desconto=request.POST.get("desconto"),
            acressimo=request.POST.get("acressimo"),
            total=request.POST.get("total"),
            modo_pgto=request.POST.get("modo_pgto"),
            data_alteracao=datetime.now().date().strftime("%Y-%m-%d"),
            pgto_adiantado=pgto_adiantado,
            os_finalizada=os_finalizada,
        )

        # if not client.objects.filter(pk=request.POST.get("cod_cli")).exists():
        work_orders.save()
        messages.add_message(request, constants.SUCCESS,
                             'Nova ordem se serviço cadastrado com sucesso')
        return redirect('work_order')
    else:
        return HttpResponseBadRequest('Invalid request method')


@login_required
def edit_work_order(request, id):
    list_client = client.objects.all()
    list_employee = Employees.objects.all()
    list_service = Services.objects.all()

    try:
        service = Services.objects.get(cod=id)
    except:
        service = ""
    try:
        tipo = Services.objects.get(cod=id).tipo
    except:
        tipo = ""
        
    print(service, tipo)    
    if request.method == "GET":
        return render(request, 'edit_work_order.html', {
            'id': id,
            'list_client': list_client,
            'list_employee': list_employee,
            'list_service': list_service,
            'nome': work_order_model.objects.get(id=id).cod_cli.nome,
            'whatsapp': work_order_model.objects.get(id=id).whatsapp,
            'data_entrada': work_order_model.objects.get(id=id).data_entrada,
            'hora_entrada': work_order_model.objects.get(id=id).data_entrada.strftime("%H:%M"),
            'cod_cli': work_order_model.objects.get(id=id).cod_cli.cod_cli,
            'cod_tec': work_order_model.objects.get(id=id).cod_tec,
            'cod_ser': work_order_model.objects.get(id=id).cod_ser,
            'cod_user': work_order_model.objects.get(id=id).cod_user,
            'whatsapp': work_order_model.objects.get(id=id).whatsapp,
            'status': work_order_model.objects.get(id=id).status,
            'obs_cli': work_order_model.objects.get(id=id).obs_cli,
            'produto': work_order_model.objects.get(id=id).produto,
            'marca': work_order_model.objects.get(id=id).marca,
            'modelo': work_order_model.objects.get(id=id).modelo,
            'serie': work_order_model.objects.get(id=id).serie,
            'condicao': work_order_model.objects.get(id=id).condicao,
            'acessorios': work_order_model.objects.get(id=id).acessorios,
            'defeito': work_order_model.objects.get(id=id).defeito,
            'obs_ser': work_order_model.objects.get(id=id).obs_ser,
            'solucao': work_order_model.objects.get(id=id).solucao,
            'servico': service,
            'servico_tipo': tipo,
            'preco': work_order_model.objects.get(id=id).preco,
            'desconto': work_order_model.objects.get(id=id).desconto,
            'acressimo': work_order_model.objects.get(id=id).acressimo,
            'total': work_order_model.objects.get(id=id).total,
            'modo_pgto': work_order_model.objects.get(id=id).modo_pgto,
            'pgto_adiantado': work_order_model.objects.get(id=id).pgto_adiantado,
            'os_finalizada': work_order_model.objects.get(id=id).os_finalizada,
            'data_entrada': work_order_model.objects.get(id=id).data_entrada.strftime("%Y-%m-%d"),
            'data_saida': work_order_model.objects.get(id=id).data_saida,
            'data_alteracao': datetime.now().date()
        })

    if request.method == "POST":
        
        work_orders = work_order_model.objects.get(id=id)
            
        work_orders.cod_cli=client.objects.get(pk=request.POST.get("cod_cli"))
        work_orders.cod_tec=Employees.objects.get(pk=request.POST.get("cod_tecnico"))
        work_orders.cod_ser=Services.objects.get(cod=id)
        work_orders.cod_user=request.user
        work_orders.whatsapp=request.POST.get("whatsapp")
        work_orders.status=request.POST.get("status")
        work_orders.obs_cli=request.POST.get("obs_cli")
        work_orders.produto=request.POST.get("produto")
        work_orders.marca=request.POST.get("marca")
        work_orders.modelo=request.POST.get("modelo")
        work_orders.serie=request.POST.get("serie")
        work_orders.condicao=request.POST.get("condicao")
        work_orders.acessorios=request.POST.get("acessorios")
        work_orders.defeito=request.POST.get("defeito")
        work_orders.obs_ser=request.POST.get("obs_ser")
        work_orders.solucao=request.POST.get("solucao")
        work_orders.preco=request.POST.get("preco")
        work_orders.desconto=request.POST.get("desconto")
        work_orders.acressimo=request.POST.get("acressimo")
        work_orders.total=request.POST.get("total")
        work_orders.modo_pgto=request.POST.get("modo_pgto")
        work_orders.data_alteracao=datetime.now().date().strftime("%Y-%m-%d")
        work_orders.pgto_adiantado=True if request.POST.get(
            "pgto_adiantado") else False
        work_orders.os_finalizada=True if request.POST.get("os_finalizada") else False
           
        print(work_orders.cod_ser)
        work_orders.save()

        messages.success(request, 'Ordem de serviço atualizada com sucesso!')
    return redirect('work_order')



@ login_required
def del_work_order(request, id):
    order = work_order_model.objects.get(id=id)
    order.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Ordem de serviço apagada com sucesso')
    return redirect('work_order')
