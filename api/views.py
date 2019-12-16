from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import * 

from rest_framework import status

from django.contrib.auth import get_user_model
User = get_user_model()



class PalestraList(APIView):
    def get(self, request):
        palestra = Palestra.objects.all()
        data = PalestraSerializer(palestra, many=True).data
        
        return Response(data)


class PalestraDetail(APIView):
    def get(self, request, pk):
        palestra = get_object_or_404(Palestra, pk=pk)
        data = PalestraSerializer(palestra).data

        return Response(data)


class FormList(APIView):
    def get(self, request):
        form = Form.objects.all()
        data = FormSerializer(form, many=True).data
        
        return Response(data)
'''
    def post(self, request):
        autor = request.data['autor']
        id_palestra = request.data['id_palestra']
        pergunta1 = request.data['Pergunta1']
        pergunta1 = request.data['Pergunta2']
        pergunta1 = request.data['Pergunta3']
        pergunta1 = request.data['Pergunta4']
        pergunta1 = request.data['Pergunta5']

        form = Form(autor=autor, id_palestra=id_palestra, pergunta1=pergunta1,pergunta2=pergunta2,pergunta3=pergunta3,pergunta4=pergunta4,pergunta5=pergunta5)
        postagem.save()
        data = PostagemSerializer(postagem).data
        return Response(data)
'''

class FormDetail(APIView):
    def get(self, request, pk):
        form = get_object_or_404(Form, pk=pk)
        data = FormSerializer(form).data

        return Response(data)


class UserList(APIView):
    permission_classes = [IsAdminUser] #DEVE SER ADMIN PARA VER DADOS DOS USUARIOS

    def get(self, request):
        user = User.objects.all()
        data = UserSerializer(user, many=True).data
        
        return Response(data)

class UserDetail(APIView):
    permission_classes = [IsAdminUser] #DEVE SER ADMIN PARA VER DADOS DO USUARIO

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        data = UserSerializer(user).data

        return Response(data)


class UserCreate(generics.CreateAPIView):
    permission_classes = [IsAdminUser] #DEVE SER ADMIN PARA CRIAR O USUÁRIO, POIS QUEREMOS QUE A PESSOA VÁ À BANCADA
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Senha incorreta"}, status=status.HTTP_400_BAD_REQUEST)
