from django.urls import path
from . import views
urlpatterns = [
    #students
    path('students/', views.list_students,name='all_students'),
    path('students/<int:pk>/', views.get_student,name='single_student'),
    #employees
    path('employees/',views.Employees.as_view()),
    path('employees/<int:pk>/',views.EmployeeDetail.as_view()),

    #books
    path('books/',views.all_books,name = 'all_books'),
    path('books/<int:pk>/',views.get_update_delete,name = 'single_book'),

    #clothes
    path('clothes/',views.Clothes.as_view(),name='all_clothes'),
    path('clothes/<int:pk>/',views.ClothDetail.as_view(),name='get_clothes'),
    
]