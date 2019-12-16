from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
User = get_user_model()


class PalestraSerializer(serializers.ModelSerializer):

    class Meta:

        model = Palestra
        fields = '__all__'

class FormSerializer(serializers.ModelSerializer):

    #owner=

    class Meta:

        model = Form
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    #form = serializers.PrimaryKeyRelatedField(many=True,queryset=Form.objects.all())

    class Meta:

        model = User
        fields = ('nome', 'email', 'dre', 'password')
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
        



