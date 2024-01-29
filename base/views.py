from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from base.models import Product
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


@api_view(['GET'])
def index(req):
    return Response('hello')

# login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['password'] = user.password
        # ...
        return token

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def products(req):
#     if req.method =='GET':
#         user= req.user
#         temp_task=user.product_set.all()
#         return Response(ProductSerializer(temp_task, many=True).data)



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    def create(self, validated_data):
        user = self.context['user']
        print(user)
        return Task.objects.create(**validated_data,user=user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    return Response('private zone')


@api_view(['GET'])
def test(request):
    return Response('public zone')


# register
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )
    user.is_active = True
    user.is_staff = False
    user.save()
    return Response("new user born")

# CRUD 

@api_view(['GET','POST','DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def products(request,id=None):
    if request.method == 'GET':
        if id is not None:
            temp_task=Product.objects.get(id=id)
            return Response(ProductSerializer(temp_task).data)
        else:
            temp_task=Product.objects.all()
            return Response(ProductSerializer(temp_task,many=True).data)
    elif request.method == 'POST':
        temp_task=Product.objects.create(
            user=request.user,
            desc=request.data['desc'],
            price=request.data['price']
        )
        return Response(ProductSerializer(temp_task).data)
    elif request.method == 'DELETE':
        try:
            temp_task=Product.objects.get(id=id)
            temp_task.delete()
            return Response("{'message': 'Product deleted successfully'}", status=200)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=400)

    elif request.method == 'PUT':
        temp_task=Product.objects.get(id=id)
        temp_task.desc=request.data['desc']
        temp_task.price=request.data['price']
        temp_task.save()
        return Response(ProductSerializer(temp_task).data) 











# @api_view(['GET','POST','DELETE','PUT','PATCH'])
# @permission_classes([IsAuthenticated])
# class MyModelView(APIView):
#     """
#     This class handle the CRUD operations for MyModel
#     """
#     def get(self, request):
#         """
#         Handle GET requests to return a list of MyModel objects
#         """
#         my_model = Task.objects.all()
#         serializer = TaskSerializer(my_model, many=True)
#         return Response(serializer.data)


#     def post(self, request):
#         """
#         Handle POST requests to create a new Task object
#         """
#         # usr =request.user
#         # print(usr)
#         serializer = TaskSerializer(data=request.data, context={'user': request.user})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
#     def put(self, request, pk):
#         """
#         Handle PUT requests to update an existing Task object
#         """
#         my_model = Task.objects.get(pk=pk)
#         serializer = TaskSerializer(my_model, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
#     def delete(self, request, pk):
#         """
#         Handle DELETE requests to delete a Task object
#         """
#         my_model = Task.objects.get(pk=pk)
#         my_model.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)