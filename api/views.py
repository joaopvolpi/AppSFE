from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


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