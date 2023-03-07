from django.shortcuts import render

def finance(request):
    return render(request, 'finance.html')

def new_entry(request):
    return render(request, 'new_entry.html')

def edit_entry(request):
    return render(request, 'edit_entry.html')

def del_entry(request):
    return render(request, 'del_entry.html')