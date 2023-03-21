from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, FileResponse
from django.core import management
from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.db import connection
import time
from django.contrib import messages
from django.contrib.messages import constants
from django.core import management
from io import StringIO


@user_passes_test(lambda u: u.is_superuser)
def backup(request):
    response = HttpResponse(content_type='application/x-sqlite3')
    response['Content-Disposition'] = 'attachment; filename="backup.db"'
    management.call_command('dbbackup', stdout=response)
    response = FileResponse(response, as_attachment=True)
    context = {'backup_success': True}
    return render(request, 'backup.html', context)


@user_passes_test(lambda u: u.is_superuser)
def backup_download(request):
    backup_filename = 'backup.dump'
    backup_path = os.path.join('media', 'backup', backup_filename)

    management.call_command('dbbackup', output_path=backup_path)

    if os.path.exists(backup_path):
        with open(backup_path, 'rb') as f:
            response = HttpResponse(
                f.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
            messages.add_message(request, constants.SUCCESS,
                                 'Backup realizado com sucesso!')
            return response
    else:
        messages.add_message(request, constants.ERROR,
                             'Erro ao efetuar o backup, Nenhum arquivo encontrado!')
        return redirect('backup')


@user_passes_test(lambda u: u.is_superuser)
def restore(request):
    backup_file = request.FILES.get('backup_file')
    confirm_restore = request.POST.get('confirm_restore')

    if backup_file and confirm_restore == "CONFIRMAR":
        connection.close()
        time.sleep(2)
        backup_path = os.path.join(
            settings.MEDIA_ROOT, 'backup', backup_file.name)
        with open(backup_path, 'wb') as f:
            for chunk in backup_file.chunks():
                f.write(chunk)

        # Add these lines to disable the prompt for confirmation
        in_buffer = StringIO('yes\n')
        out_buffer = StringIO()
        with open(backup_path, 'rb') as backup_file:
            management.call_command("dbrestore", database='default',
                                    input_filename=backup_path, interactive=False)

        try:
            os.remove(backup_path)
        except PermissionError:
            # Tenta remover o arquivo várias vezes, esperando entre cada tentativa
            for i in range(10):
                try:
                    os.remove(backup_path)
                    break  # Sai do loop se conseguir remover o arquivo
                except PermissionError:
                    # Espera um segundo antes de tentar novamente
                    time.sleep(1)
        try:
            time.sleep(2)
            connection.connect()
            messages.add_message(request, constants.SUCCESS,
                                 'Backup Restaurado com sucesso!')
            return redirect('backup')
        except Exception as e:
            messages.add_message(request, constants.ERROR,
                                 f'Erro ao restaurar backup: {str(e)}, status=500')
            return redirect('backup')
    elif backup_file:
        messages.add_message(request, constants.ERROR,
                             'Por favor, confirme a restauração digitando "CONFIRMAR".')
    else:
        messages.add_message(request, constants.ERROR,
                             'Nenhum arquivo de backup enviado!')
    return redirect('backup')
