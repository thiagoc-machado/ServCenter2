from django.urls import path
from . import views
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.config, name="config"),
    path('new_config/', views.new_config, name='new_config'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)