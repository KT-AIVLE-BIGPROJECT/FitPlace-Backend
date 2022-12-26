from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from datetime import timedelta, datetime
from .serializers import *
import random


class PlacesViewSet(APIView):
    def get(self, request, format=None):
        queryset = Places.objects.all()
        serializer = PlacesSerializer(queryset, many=True)
        print(len(queryset))
        return Response(serializer.data)


class PlacesTop100ViewSet(APIView):
    def get(self, request, format=None):
        places = list(Places.objects.order_by('-review_blog_count','-review_count')[:100])
        queryset = random.sample(places,7)
        print(queryset)
        serializer = PlacesSerializer(queryset, many=True)
        print(len(queryset))
        return Response(serializer.data)


class CongestionViewSet(APIView):
    def get(self, request, format=None):
        area_nm = request.GET.get('area_nm')
        hour = datetime.today().hour
        queryset = Congestion.objects.filter(area_nm=area_nm,
                                             now__range=[datetime.today() - timedelta(days=7),
                                                         datetime.today() - timedelta(days=1)],
                                             now__hour=hour,
                                             ).order_by('-now')
        serializer = CongestionSerializer(queryset, many=True)
        print(len(queryset))
        return Response(serializer.data)
