from django.urls import path,include
from . import views
from .views import BookViewSet,ClothesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('books',BookViewSet,basename='book')
router.register('clothes',ClothesViewSet,basename='cloth')

urlpatterns = [
    #students
    path('students/', views.list_students,name='all_students'),
    path('students/<int:pk>/', views.get_student,name='single_student'),
    #employees
    path('employees/',views.Employees.as_view()),
    path('employees/<int:pk>/',views.EmployeeDetail.as_view()),

    #books
    # path('books/',views.all_books,name = 'all_books'),
    # path('books/<int:pk>/',views.get_update_delete,name = 'single_book'),
    path('',include(router.urls)),

    #clothes
    path('clothes/',views.Clothes.as_view(),name='all_clothes'),
    path('clothes/<int:pk>/',views.ClothDetail.as_view(),name='get_clothes'),
    
]