from rest_framework import serializers
from .models import *


class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = '__all__'


class CongestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Congestion
        fields = '__all__'
