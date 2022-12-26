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
# class PlacesViewSet(APIView):
#     def get(self, request, format=None):
#         queryset = Places.objects.all()
#         serializer = PlacesSerializer(queryset, many=True)
#         print(len(queryset))
#         return Response(serializer.data)
class PlacesViewSet(generics.ListAPIView):
    queryset = Places.objects.all()#.order_by('-place_rating')
    serializer_class = PlacesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['place_category', 'id']

class PlacesTop100ViewSet(APIView):
    def get(self, request, format=None):
        places = list(Places.objects.order_by('-review_blog_count','-review_count')[:100])
        queryset = random.sample(places,7)
        print(queryset)
        serializer = PlacesSerializer(queryset, many=True)
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
