from rest_framework import serializers
from .models import *


class PalestraSerializer(serializers.ModelSerializer):

    class Meta:

        model = Palestra
        fields = '__all__'