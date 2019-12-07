from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class PalestraSerializer(serializers.ModelSerializer):

    class Meta:

        model = Palestra
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        def create(self, validated_data):
            user = User(
                username=validated_data['email'],
                
            )
            
            user.set_password(validated_data['password'])
            user.save()
            return user 