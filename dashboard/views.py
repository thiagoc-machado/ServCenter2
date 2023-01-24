from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')
