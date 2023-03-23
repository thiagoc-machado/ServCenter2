from django.urls import path
from . import views
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from .models import Config

if Config.objects.exists():
    urlpatterns = [
        path('', views.config, name="config"),
        path('edit/', views.edit_config, name="edit_config"),
    ] 
else:
    urlpatterns = [
        path('', views.new_config, name='new_config'),
    ] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)