from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.finance, name="finance"),
    path('new_entry/', views.new_entry, name="new_entry"),
    path('del_entry/', views.del_entry, name="del_entry"),
    path('edit_entry/', views.edit_entry, name='edit_entry'),

]