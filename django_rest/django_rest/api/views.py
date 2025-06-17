# from django.shortcuts import render
# from django.http import JsonResponse,HttpResponse
from students.models import students
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def list_students(request):
    # students = {
    #     'id' : 1,
    #     'name': 'Naveen',
    #     'class' : 'CS'
    # }
    # allstudents = students.objects.all()
    # student_list = list(allstudents.values())
    # return JsonResponse(student_list,safe=False)

    if request.method == 'GET':
        # get all students
        allstudents = students.objects.all()
        serializer = StudentSerializer(allstudents,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

