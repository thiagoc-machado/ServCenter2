from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.work_order, name="work_order"),
    path('new_work_order/', views.new_work_order, name="new_work_order"),
    path('edit_work_order/<int:id>', views.edit_work_order, name="edit_work_order"),
    path('del_work_order/<int:id>', views.del_work_order, name="del_work_order"),
]
