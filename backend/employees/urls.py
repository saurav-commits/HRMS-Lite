from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee-list'),
    path('<str:pk>/', views.employee_detail, name='employee-detail'),
]