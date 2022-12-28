from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views import View

from .models import *
from datetime import timedelta, datetime
from .serializers import *
import random
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

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

# [ 사용자 별 맞춤 장소 불러오기 ]
# - 중분류 카테고리별, 지역구별 필터링
# - 평점순, 리뷰순 정렬
class RecommendationAPI(APIView):
    def post(self, request):
        # 사용자 입력정보 데이터 받아오기
        userform = json.loads(request.body)
        userform = pd.DataFrame([userform])
        print(f"사용자 특성,취향 파라미터")
        print(userform)
        #print(userform.columns)
        # print(type(userform))
        # 장소 추천 파라미터 데이터 받아오기
        recParams = RecParam.objects.all()
        recParams_df = pd.DataFrame.from_records(recParams.values())
        recParams_df = recParams_df.drop(columns=['id'])
        # 장소 데이터 받아오기
        places = Place.objects.all()
        places_df = pd.DataFrame.from_records(places.values())
        
        # 사용자 입력 정보 - 장소 데이터 간의 코사인 유사도 구하기
        recommend_places = pd.DataFrame(cosine_similarity(
            userform,
            recParams_df.loc[ : , recParams_df.columns != 'place_code' ]),
            columns = list(recParams_df.place_code), index=['similarity']
        )
        
        # 유사도 순서대로 정렬
        topN = recommend_places.T.sort_values('similarity', ascending=False)
        topN_df = pd.DataFrame({
            'place_code': list(topN.index)
        })
        # 장소id로 장소 데이터와 INNER JOIN ==> 최종 추천 장소 목록
        final_recommends = pd.merge(topN_df, places_df, how='left', on='place_code')
        print("유사도 순으로 추천된 장소들입니다.")
        print(final_recommends) # 상위 30개 정도까진 같은데 그 다음부터는 주피터 노트북이나 장고 쉘하고 결과가 다름;;
        # print(final_recommends[:200]['search_category'].value_counts())
        
        # recommend_response = final_recommends.to_records()
        # print(recommend_response)
        
        # serializer = RecParamSerializer(queryset, many=True)
        return Response(final_recommends)
        
            


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
