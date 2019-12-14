from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

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


class FormDetail(APIView):
    def get(self, request, pk):
        form = get_object_or_404(Form, pk=pk)
        data = FormSerializer(form).data

        return Response(data)


class UserList(APIView):
    def get(self, request):
        user = User.objects.all()
        data = UserSerializer(user, many=True).data
        
        return Response(data)

class UserDetail(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        data = UserSerializer(user).data

        return Response(data)