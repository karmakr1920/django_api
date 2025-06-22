from rest_framework import serializers
from students.models import students
from employee.models import Employee
from books.models import Book
from clothes.models import Cloth
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = students
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = '__all__'