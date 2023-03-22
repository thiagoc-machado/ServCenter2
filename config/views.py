from django.shortcuts import render
from django.shortcuts import render
from .forms import ConfigForm
from .models import Config

def config(request):
    configs = Config.objects.all()
    return render(request, 'config.html', {'configs': configs})



def new_config(request):
    form = ConfigForm()
    if request.method == 'POST':
        form = ConfigForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'new_config.html', {'form': form})

