from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Services, User, client, Employees, work_order as work_order_model, image
from finance.models import Finance
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import pytz

br_tz = pytz.timezone('America/Sao_Paulo')
time_br = datetime.now(br_tz).time()

@login_required
def work_order(request):
    if request.method == "GET":
        workorders = work_order_model.objects.all()
        return render(request, 'work_order.html', {'workorders': workorders})
    else:
        return HttpResponseBadRequest('Invalid request method')


@login_required
def new_work_order(request):

    if request.method == "GET":
        list_client = client.objects.all()
        list_employee = Employees.objects.all()
        list_service = Services.objects.all()
        list_client = client.objects.all()
        user=request.user

        try:
            service = Services.objects.get(cod=id)
        except:
            service = ""
        try:
            tipo = Services.objects.get(cod=id).tipo
        except:
            tipo = ""
        hora = datetime.now().time()
        data = datetime.now().date().strftime("%Y-%m-%d")
        print(data)

        return render(request, 'new_work_order.html', {'list_client': list_client,
                                                       'list_employee': list_employee,
                                                       'list_service': list_service,
                                                       'data': data,
                                                       'hora': hora,
                                                       'user': user,
                                                       })

    elif request.method == "POST":

        if request.POST.get("pgto_adiantado") == None:
            pgto_adiantado = False
        else:
            pgto_adiantado = True
        if request.POST.get("os_finalizada") == None:
            os_finalizada = False
        else:
            os_finalizada = True

        cod_cli_str = request.POST.get("cod_cli")

        if not cod_cli_str:
            # Se o cod_cli estiver vazio, cria um novo objeto 'client'
            message = True
            nome = request.POST.get("cliente")
            whatsapp = request.POST.get("whatsapp")
            client_obj, created = client.objects.get_or_create(
                nome=nome,
                whatsapp=whatsapp,
                vendedor=request.user,
                data_nasc="1900-01-01",
                ativo=True,
            )
        else:
            message = False
            client_obj = client.objects.get(pk=cod_cli_str)
    
        work_orders = work_order_model(
            # Services.objects.get(cod=id)
            cod_cli=client_obj,
            cod_tec=Employees.objects.get(
                pk=request.POST.get("cod_tecnico")),
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
            photos=request.FILES.getlist('photos')
        )
        # if not client.objects.filter(pk=request.POST.get("cod_cli")).exists():
        if 'photos' in request.FILES:
        # percorre cada imagem enviada
            for photo in request.FILES.getlist('photos'):
                # cria um objeto image para cada imagem enviada
                image_obj = image(
                    photo=photo,
                    order=work_orders
                )
                image_obj.save()
        work_orders.save()
        
        
        if pgto_adiantado == True and request.POST.get("total") != '':

            finances = Finance.objects.all()

            obs = 'Pagamento adiantado da OS: ' + str(work_orders)
            nome = client.objects.get(pk=request.POST.get("cod_cli")).nome
            data = datetime.now().date().strftime("%Y-%m-%d")
            valor = request.POST.get("total")
            movimento = 'entrada'

            finances = Finance(
                obs=obs,
                nome=nome,
                data=data,
                valor=valor,
                movimento=movimento,
                hora = time_br
            )
            finances.save()

            if message == True:
                messages.add_message(request, constants.SUCCESS,
                                        'Nova ordem de serviço criada, novo cliente cadastrado com sucesso e pagamento lançado no financeiro')
            else:
                messages.add_message(request, constants.SUCCESS,
                                        'Nova ordem de serviço criada com sucesso e pagamento lançado no financeiro')
        else:
            if message == True:
                messages.add_message(request, constants.SUCCESS,
                                        'Nova ordem de serviço criada e novo cliente cadastrado com sucesso')
            else:
                messages.add_message(request, constants.SUCCESS,
                                        'Nova ordem de serviço criada com sucesso')

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

    if request.method == "GET":
        
        order = work_order_model.objects.get(id=id)
        fotos = image.objects.filter(order_id=id)
        # print(Services.objects.get(cod=id) )
        return render(request, 'edit_work_order.html', {
            'fotos': fotos,
            'id': id,
            'list_client': list_client,
            'list_employee': list_employee,
            'list_service': list_service,
            'nome': work_order_model.objects.get(id=id).cod_cli.nome,
            'whatsapp': work_order_model.objects.get(id=id).whatsapp,
            'data_entrada': work_order_model.objects.get(id=id).data_entrada,
            'hora_entrada': work_order_model.objects.get(id=id).data_entrada.strftime("%H:%M"),
            'cod_os': work_order_model.objects.get(id=id).pk,
            'cod_cli': work_order_model.objects.get(id=id).cod_cli.pk,
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
            'data_alteracao': datetime.now().date(),
        })

    if request.method == "POST":

        pago = work_order_model.objects.get(id=id).pgto_adiantado

        work_orders = work_order_model.objects.get(id=id)

        work_orders.cod_cli = client.objects.get(
            pk=request.POST.get("cod_cli"))
        work_orders.cod_tec = Employees.objects.get(
            pk=request.POST.get("cod_tecnico"))
        work_orders.cod_ser = Services.objects.get(
            pk=request.POST.get("cod_ser"))

        work_orders.cod_user = request.user
        work_orders.whatsapp = request.POST.get("whatsapp")
        work_orders.status = request.POST.get("status")
        work_orders.obs_cli = request.POST.get("obs_cli")
        work_orders.produto = request.POST.get("produto")
        work_orders.marca = request.POST.get("marca")
        work_orders.modelo = request.POST.get("modelo")
        work_orders.serie = request.POST.get("serie")
        work_orders.condicao = request.POST.get("condicao")
        work_orders.acessorios = request.POST.get("acessorios")
        work_orders.defeito = request.POST.get("defeito")
        work_orders.obs_ser = request.POST.get("obs_ser")
        work_orders.solucao = request.POST.get("solucao")
        work_orders.preco = request.POST.get("preco")
        work_orders.desconto = request.POST.get("desconto")
        work_orders.acressimo = request.POST.get("acressimo")
        work_orders.total = request.POST.get("total")
        work_orders.modo_pgto = request.POST.get("modo_pgto")
        work_orders.data_alteracao = datetime.now().date().strftime("%Y-%m-%d")
        work_orders.pgto_adiantado = True if request.POST.get(
            "pgto_adiantado") and request.POST.get("total") != '' else False
        work_orders.os_finalizada = True if request.POST.get(
            "os_finalizada") else False
        
        if 'photos' in request.FILES:
        # percorre cada imagem enviada
            for photo in request.FILES.getlist('photos'):
                # cria um objeto image para cada imagem enviada
                image_obj = image(
                    photo=photo,
                    order=work_orders
                )
                image_obj.save()
        
        work_orders.save()

        if work_order_model.objects.get(id=id).pgto_adiantado == True and request.POST.get("total") != '' and pago == False:

            finances = Finance.objects.all()

            obs = 'Pagamento adiantado da OS: ' + str(work_orders)  # .cod
            nome = client.objects.get(pk=request.POST.get("cod_cli")).nome
            data = datetime.now().date().strftime("%Y-%m-%d")
            valor = request.POST.get("total")
            movimento = 'entrada'

            finances = Finance(
                obs=obs,
                nome=nome,
                data=data,
                valor=valor,
                movimento=movimento,
                hora = time_br
            )
            finances.save()

            messages.add_message(request, constants.SUCCESS,
                                 'Nova ordem se serviço editada com sucesso e pagamento lançado no financeiro')
        else:
            messages.add_message(request, constants.SUCCESS,
                                 'Nova ordem se serviço editada com sucesso')

        return redirect('work_order')
    else:
        return HttpResponseBadRequest('Invalid request method')


@ login_required
def del_work_order(request, id):
    order = work_order_model.objects.get(id=id)
    order.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Ordem de serviço apagada com sucesso')
    return redirect('work_order')
