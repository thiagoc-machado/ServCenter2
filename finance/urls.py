from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.finance, name="finance"),
    path('new_finance/', views.new_finance, name="new_finance"),
    path('new_finance_out/', views.new_finance_out, name="new_finance_out"),
    path('del_finance/', views.del_finance, name="del_finance"),
    path('edit_finance/', views.edit_finance, name='edit_finance')
]