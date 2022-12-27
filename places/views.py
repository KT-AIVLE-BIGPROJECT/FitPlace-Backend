from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from datetime import timedelta, datetime
from .serializers import *
import random

# # [ 전체 장소 불러오기 + 카테고리 지정 ]
# class PlaceViewSet(APIView):
#     def get(self, request, format=None):
#         queryset = Place.objects.all()
#         serializer = PlaceSerializer(queryset, many=True)
#         print(len(queryset))
#         return Response(serializer.data)
class PlaceViewSet(generics.ListAPIView):
    queryset = Place.objects.all()#.order_by('-rating')
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['search_category']

class PlaceTop100ViewSet(APIView):
    def get(self, request, format=None):
        places = list(Place.objects.order_by('-review_blog_count','-review_visitor_count')[:100])
        queryset = random.sample(places,7)
        print(queryset)
        serializer = PlaceSerializer(queryset, many=True)
        print(len(queryset))
        return Response(serializer.data)

# class RecommendationAPI(APIView):
#     def post(self, request):
#         serializers = 


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
