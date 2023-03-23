from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

@login_required
def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html') 

    else:
        return HttpResponseBadRequest('Invalid request method')