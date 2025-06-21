from django.urls import path
from . import views
urlpatterns = [
    path('students/', views.list_students,name='all_students'),
    path('students/<int:pk>/', views.get_student,name='single_student'),
    
    path('employees/',views.Employees.as_view()),
    path('employees/<int:id>/',views.EmployeeDetail.as_view())
    
]