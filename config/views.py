from django.shortcuts import render
from django.shortcuts import render
from .forms import ConfigForm
from .models import Config
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def config(request):
    configs = Config.objects.all()
    return render(request, 'config.html', {'configs': configs})


@user_passes_test(lambda u: u.is_superuser)
def new_config(request):
    form = ConfigForm()
    if request.method == 'POST':
        form = ConfigForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'new_config.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def edit_config(request):
    config = Config.objects.get(pk=2)
    form = ConfigForm(instance=config)
    if request.method == 'POST':
        form = ConfigForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
    return render(request, 'edit_config.html', {'form': form})

