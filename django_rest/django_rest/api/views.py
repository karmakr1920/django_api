# from django.shortcuts import render
# from django.http import JsonResponse,HttpResponse
from students.models import students
from .serializers import StudentSerializer,EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employee.models import Employee
from django.http import Http404
@api_view(['GET','POST'])
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
    elif request.method == 'POST':
        serializer = StudentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def get_student(request, pk):
    try:
        single_student = students.objects.get(id=pk)
    except students.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(single_student)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(single_student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        single_student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Employees(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class EmployeeDetail(APIView):
    def get_object(self,id):
        try:
            return Employee.objects.get(id = id)
        except Employee.DoesNotExist:
            raise Http404
        
    def get(self,request,id):
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id):
        employee = Employee.objects.get(id = id)
        serializer = EmployeeSerializer(employee,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        employee = self.get_object(id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)