from rest_framework import serializers
from students.models import students
from employee.models import Employee

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = students
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'