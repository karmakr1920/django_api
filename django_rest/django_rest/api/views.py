from django.shortcuts import render,get_object_or_404
# from django.http import JsonResponse,HttpResponse
from students.models import students
from employee.models import Employee
from books.models import Book
from clothes.models import Cloth
from blogs.models import Blog,Comment
from .serializers import StudentSerializer,EmployeeSerializer,BookSerializer,ClothSerializer
from blogs.serializers import BlogSerializer,CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins,generics,viewsets
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

"""
# Class based approach
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

"""
class Employees(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)
    
class EmployeeDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    #lookup_field = 'id'  # if you use other than pk
    def get(self,request,pk):
        return self.retrieve(request,pk)
    
    def put(self,request,pk):
        return self.update(request,pk)
    
    def delete(self,request,pk):
        return self.destroy(request,pk)
    
@api_view(['GET','POST'])
def all_books(request):
    if request.method == 'GET':
        book_list = Book.objects.all()
        serializer = BookSerializer(book_list,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def get_update_delete(request,pk):
    try:
        single_book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BookSerializer(single_book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookSerializer(single_book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        single_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
"""
# Class Based approach
class Clothes(APIView):
    
    def get(self,request):
        all_clothes = Cloth.objects.all()
        serializer = ClothSerializer(all_clothes,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ClothSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ClothDetail(APIView):
    def get_object(self,pk):
        try:
            return Cloth.objects.get(pk = pk)
        except Cloth.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,pk):
        single_cloth = self.get_object(pk)
        serializer = ClothSerializer(single_cloth)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        update_cloth = self.get_object(pk)
        serializer = ClothSerializer(update_cloth,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        delete_cloth = self.get_object(pk)
        delete_cloth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

"""
# Mixins start
class Clothes(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)

class ClothDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
    def get(self,request,pk):
        return self.retrieve(request,pk)
    def put(self,request,pk):
        return self.update(request,pk)
    
    def delete(self,request,pk):
        return self.destroy(request,pk)

# Mixins End
"""
# Generics start
"""
-> ListAPIView: Provides a read-only endpoint to list all objects (GET).
-> CreateAPIView: Provides an endpoint to create a new object (POST).
-> RetrieveAPIView: Provides a read-only endpoint to retrieve a single object (GET with pk).
-> UpdateAPIView: Provides an endpoint to update an existing object (PUT or PATCH with pk).
-> DestroyAPIView: Provides an endpoint to delete an object (DELETE with pk).
-> ListCreateAPIView: Combines listing all objects and creating new ones (GET + POST).
-> RetrieveUpdateDestroyAPIView: Combines retrieve, update, and delete for a single object (GET, PUT, PATCH, DELETE with pk).

"""
class Clothes(generics.ListCreateAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

class ClothDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
    lookup_field = 'pk'

class BookViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def create(self,request):
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk= None):
        book = get_object_or_404(Book,pk =pk)
        serializer = BookSerializer(book)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def update(self,request,pk=None):
        book = get_object_or_404(Book,pk =pk)
        serializer = BookSerializer(book,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk=None):
        book = get_object_or_404(Book,pk =pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'
class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'