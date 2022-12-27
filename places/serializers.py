from rest_framework import serializers
from .models import *


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class RecParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecParam
        fields = '__all__'
        
class CongestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Congestion
        fields = '__all__'


# class RecommendationSerializer()