from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class PalestraSerializer(serializers.ModelSerializer):

    class Meta:

        model = Palestra
        fields = '__all__'

class FormSerializer(serializers.ModelSerializer):

    class Meta:

        model = Form
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('nome','email','dre')



