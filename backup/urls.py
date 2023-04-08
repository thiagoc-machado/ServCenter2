from django.urls import path
from . import views

urlpatterns = [
    path('', views.backup, name='backup'),
    path('backup/download/', views.backup_download, name='backup_download'),
    path('restore/', views.restore, name='restore'),
    path('export_to_excel/', views.export_to_excel, name='export_to_excel'),
]
