from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
User = get_user_model()
from .views import *
from .models import *

class PalestraSerializer(serializers.ModelSerializer):

    #favorito = serializers.StringRelatedField(many=True)  
    #user =  self.context['request'].user

    class Meta:

        model = Palestra
        exclude = ['foi_na_palestra', 'favorito']
        

class FormSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        
        model = Form
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('nome', 'email', 'dre', 'password', "foto_perfil")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            nome=validated_data['nome'],
            dre=validated_data['dre'],

        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
        



