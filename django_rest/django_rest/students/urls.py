from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='home'),
    path('', views.get_students,name='all_students'),
]