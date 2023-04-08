# from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
# from PIL import Image
# from documents.models import Documents

# def miniatura(request, id):
#     arquivo = get_object_or_404(Documents,id=id)
#     imagem = Image.open(arquivo.arquivo)
#     imagem.thumbnail((128, 128))
#     response = HttpResponse(content_type="image/jpeg")
#     imagem.save(response, "JPEG")
#     return response

def documents(request):  
    return render(request, 'documents.html')

    