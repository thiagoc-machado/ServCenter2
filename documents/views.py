from django.shortcuts import render

def documents(request):
    return render(request, 'documents.html')
