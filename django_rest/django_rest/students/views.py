from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

def index(request):
    return HttpResponse('Learn DRF with Naveen')
def get_students(request):
    students = {
        'id' : 1,
        'name': 'Naveen',
        'class' : 'CS'
    }
    return JsonResponse(students)
