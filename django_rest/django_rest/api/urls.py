from django.urls import path
from . import views
urlpatterns = [
    path('students/', views.list_students,name='all_students'),
]