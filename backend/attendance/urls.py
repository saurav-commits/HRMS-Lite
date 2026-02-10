from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance-list'),
    path('summary/<str:employee_id>/', views.employee_attendance_summary, name='employee-attendance-summary'),
]