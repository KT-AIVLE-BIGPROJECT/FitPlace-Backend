from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views import View
from django.conf import settings

from .models import *
from datetime import timedelta, datetime
from .serializers import *
import random
import json
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
import time
from bs4 import BeautifulSoup # pip install beautifulsoup4
from selenium import webdriver # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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
    filterset_fields = ['place_code']

class PlaceTop100ViewSet(APIView):
    def get(self, request, format=None):
        places = list(Place.objects.order_by('-review_blog_count','-review_visitor_count')[:100])
        queryset = random.sample(places,7)
        print(queryset)
        serializer = PlaceSerializer(queryset, many=True)
        print(len(queryset))
        return Response(serializer.data)


#### [ 사용자 별 맞춤 장소 불러오기 ]
# - 중분류 카테고리별, 지역구별 필터링
# - 평점순, 리뷰순 정렬
class RecommendationAPI(APIView):
    def post(self, request):
        
        # 사용자 입력정보 데이터 받아오기
        body = json.loads(request.body)
        userform = body["userform"]
        effect_flag = body["effect_flag"]
        
        if effect_flag == -1:
            return Response(0)
        else:
            main_category = body["main_category"]
            sub_category = body["sub_category"]
            filter_rating = body["filter_rating"]
            filter_review = body["filter_review"]
            filter_region = body["filter_region"]
            
            userform = pd.DataFrame([userform])
            print(f"사용자 특성,취향 파라미터")
            print(userform)
            
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
            
            ### 지역구 필터링
            if filter_region == "강남구":
                final_recommends = final_recommends.loc[(final_recommends['search_region']=="강남구")]
            elif filter_region == "구로구":
                final_recommends = final_recommends.loc[(final_recommends['search_region']=="구로구")]
            elif filter_region == "마포구":
                final_recommends = final_recommends.loc[(final_recommends['search_region']=="마포구")]
            elif filter_region == "용산구":
                final_recommends = final_recommends.loc[(final_recommends['search_region']=="용산구")]
            elif filter_region == "종로구":
                final_recommends = final_recommends.loc[(final_recommends['search_region']=="종로구")]
                
            final_recommends_response = final_recommends
            
            # recommend_response = final_recommends.to_records()
            # print("************************************")
            # print(recommend_response)
                
            
            #### 대분류 카테고리(키워드) 선택
            if main_category == "restaurant": # "먹기" 선택
                final_recommends_response = final_recommends.loc[(final_recommends['search_category']=="한식") | (final_recommends['search_category']=="양식") |
                                                        (final_recommends['search_category']=="중식") | (final_recommends['search_category']=="일식") |
                                                        (final_recommends['search_category']=="패스트푸드") | (final_recommends['search_category']=="분식")]
            elif main_category == "cafe": # "마시기" 선택
                final_recommends_response = final_recommends.loc[(final_recommends['search_category']=="카페") | (final_recommends['search_category']=="디저트카페") |
                                                        (final_recommends['search_category']=="베이커리")]
            elif main_category == "leisure": # "놀기" 선택
                final_recommends_response = final_recommends.loc[(final_recommends['search_category']=="전시관") | (final_recommends['search_category']=="공방") |
                                                        (final_recommends['search_category']=="팝업스토어") | (final_recommends['search_category']=="극장") |
                                                        (final_recommends['search_category']=="서점") | (final_recommends['search_category']=="복합쇼핑몰")]
            elif main_category == "walking":
                final_recommends_response = final_recommends.loc[(final_recommends['search_category']=="공원") | (final_recommends['search_category']=="시장") |
                                                        (final_recommends['search_category']=="거리")]
            else:
                pass

            ### 중분류 카테고리(키워드) 선택
            if sub_category == "":
                pass
            else:
                final_recommends_response = final_recommends_response.loc[final_recommends_response['search_category'] == sub_category]
            
            #### 평점 필터링
            if filter_rating == 1: # 높은 순
                final_recommends_response = final_recommends_response.sort_values(by='rating', ascending=False)
            elif filter_rating == 2: # 낮은 순
                final_recommends_response = final_recommends_response.sort_values(by='rating', ascending=True)
            else:
                pass
            #### 리뷰 필터링
            if filter_review == 1: # 높은 순
                final_recommends_response = final_recommends_response.sort_values(by='review_visitor_count', ascending=False)
            elif filter_review == 2: # 낮은 순
                final_recommends_response = final_recommends_response.sort_values(by='review_visitor_count', ascending=True)
            else:
                pass
            
            print("유사도 순으로 추천된 장소들입니다.")
            print(main_category)
            print(final_recommends_response)
            return Response(final_recommends_response)


# [ 메인화면 연령대, 성별, MBTI 별 상위 100개 추천장소 불러오기 ]
class MainTopRecommendAPI(APIView):
    def post(self, request):
        
        # 사용자 입력정보 데이터 받아오기
        body = json.loads(request.body)
        userform = body["userform"]
        # effect_flag = body["effect_flag"]
        
        main_category = body["main_category"]
        sub_category = body["sub_category"]
        filter_rating = body["filter_rating"]
        filter_review = body["filter_review"]
        filter_region = body["filter_region"]
        
        userform = pd.DataFrame([userform])
        print(f"사용자 특성,취향 파라미터")
        print(userform)
        
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
        
        ### 지역구 필터링
        if filter_region == "강남구":
            final_recommends = final_recommends.loc[(final_recommends['search_region']=="강남구")]
        elif filter_region == "구로구":
            final_recommends = final_recommends.loc[(final_recommends['search_region']=="구로구")]
        elif filter_region == "마포구":
            final_recommends = final_recommends.loc[(final_recommends['search_region']=="마포구")]
        elif filter_region == "용산구":
            final_recommends = final_recommends.loc[(final_recommends['search_region']=="용산구")]
        elif filter_region == "종로구":
            final_recommends = final_recommends.loc[(final_recommends['search_region']=="종로구")]
            
        final_recommends_response = final_recommends
        
        # recommend_response = final_recommends.to_records()
        # print("************************************")
        # print(recommend_response)
            
        
        #### 대분류 카테고리(키워드) 선택
        if main_category == "restaurant": # "먹기" 선택
            final_recommends_response = final_recommends.loc[(final_recommends['search_category']=="한식") | (final_recommends['search_category']=="양식") |
                                                    (final_recommends['search_category']=="중식") | (final_recommends['search_category']=="일식") |
                                                    (final_recommends['search_category']=="패스트푸드") | (final_recommends['search_category']=="분식")]
        elif main_category == "cafe": # "마시기" 선택
            final_recommends_response = final_recommends.loc[(final_recommends['search_category']=="카페") | (final_recommends['search_category']=="디저트카페") |
                                                    (final_recommends['search_category']=="베이커리")]
        elif main_category == "leisure": # "놀기" 선택
            final_recommends_response = final_recommends.loc[(final_recommends['search_category']=="전시관") | (final_recommends['search_category']=="공방") |
                                                    (final_recommends['search_category']=="팝업스토어") | (final_recommends['search_category']=="극장") |
                                                    (final_recommends['search_category']=="서점") | (final_recommends['search_category']=="복합쇼핑몰")]
        elif main_category == "walking":
            final_recommends_response = final_recommends.loc[(final_recommends['search_category']=="공원") | (final_recommends['search_category']=="시장") |
                                                    (final_recommends['search_category']=="거리")]
        else:
            pass

        ### 중분류 카테고리(키워드) 선택
        if sub_category == "":
            pass
        else:
            final_recommends_response = final_recommends_response.loc[final_recommends_response['search_category'] == sub_category]
        
        #### 평점 필터링
        if filter_rating == 1: # 높은 순
            final_recommends_response = final_recommends_response.sort_values(by='rating', ascending=False)
        elif filter_rating == 2: # 낮은 순
            final_recommends_response = final_recommends_response.sort_values(by='rating', ascending=True)
        else:
            pass
        #### 리뷰 필터링
        if filter_review == 1: # 높은 순
            final_recommends_response = final_recommends_response.sort_values(by='review_visitor_count', ascending=False)
        elif filter_review == 2: # 낮은 순
            final_recommends_response = final_recommends_response.sort_values(by='review_visitor_count', ascending=True)
        else:
            pass
        
        print("유사도 순으로 추천된 장소들입니다.")
        print(main_category)
        print(final_recommends_response)
        final_recommends_response = final_recommends_response[:100]
        return Response(final_recommends_response)       


#### 혼잡도 데이터 불러오기
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
    
    
# 혼잡도 예측 API
# [ 메인화면 연령대, 성별, MBTI 별 상위 100개 추천장소 불러오기 ]
class PredictCongestion(APIView):
    def post(self, request):
        
        # 사용자 입력정보 데이터 받아오기
        body = json.loads(request.body)
        now_congestion = body["now_congestion"]
        
        now_congestion = pd.DataFrame([now_congestion])
        print(f"현재 혼잡도")
        print(now_congestion)
        
        # 모델 불러오기

        # 예측
        

        print("혼잡도 예측 결과입니다.")
        # print(predict_result)
        # return Response(predict_result)
        return Response(0)
    

# 네이버 블로그 리뷰 API
class BlogReviewAPI(APIView):
    # def get(self, request):
    #     import os
    #     return Response([os.getcwd(), os.listdir()])
    def post(self, request):
        # 사용자 입력정보 데이터 받아오기
        body = json.loads(request.body)
        place_code = body["place_code"]
        print(f"장소 코드 : {place_code}")
        
        options = webdriver.ChromeOptions()
        # 창 숨기는 옵션 추가
        options.add_argument("headless")

        # driver 실행
        driver_url = 'places/static/chromedriver.exe'
        # driver_url = 'chromedriver.exe'
        driver = webdriver.Chrome(driver_url, options=options)
        # driver = webdriver.Chrome()
        driver.implicitly_wait(5)

        blog_reviews = f"https://pcmap.place.naver.com/restaurant/{place_code}/review/ugc"
        # blog_reviews = f"https://map.naver.com/restaurant/{place_code}/review/ugc"

        driver.get(blog_reviews)

        body = BeautifulSoup(driver.page_source, 'html.parser').body

        # BLOG_REVIEW_NUM = body.select_one('em.place_section_count')
        BLOG_REVIEW_NUM = 5 # 블로그 리뷰 5개씩만
        # print(f"갖고올 블로그 리뷰 개수 : {BLOG_REVIEW_NUM}")
            
        # 리뷰 제목
        #app-root > div > div > div > div:nth-child(7) > div:nth-child(3) > div > div.place_section_content > ul > li:nth-child(1) > a > div.kT8X8 > div.hPTBw > div > span
        reviews_title = body.select('div.place_section_content > ul > li > a > div.kT8X8 > div.hPTBw > div > span')
        # print("[리뷰 제목]")
        # print(reviews_title)

        # 리뷰 내용
        #app-root > div > div > div > div:nth-child(7) > div:nth-child(3) > div > div.place_section_content > ul > li:nth-child(1) > a > div.kT8X8 > div.PRq7t > div
        reviews_body = body.select('div.place_section_content > ul > li > a > div.kT8X8 > div.PRq7t > div')
        # print("[리뷰 내용]")
        # print(reviews_body)

        # 리뷰 URL
        #app-root > div > div > div > div:nth-child(7) > div:nth-child(3) > div > div.place_section_content > ul > li:nth-child(1) > a
        reviews_url = []
        temp = body.select('div.place_section_content > ul > li > a')
        for r in temp:
            temp2 = r.attrs['href']
            reviews_url.append(temp2)
        # print("[리뷰 URL]")
        # print(reviews_url)
        
        # 리뷰 사진
        #app-root > div > div > div > div:nth-child(6) > div:nth-child(3) > div > div.place_section_content > ul > li:nth-child(1) > a > div.sxpee > div > div > div > div:nth-child(1) > span > div
        review_photos = []
        temp = body.select('div.place_section_content > ul > li > a > div.sxpee > div > div > div > div:nth-child(1) > span > div')
        for r in temp:
            temp2 = r.attrs['style']
            review_photos.append(temp2)
        # print("[리뷰 사진]")
        # print(review_photos)

        driver.quit()

        reviews_title2 = []
        reviews_body2 = []
        for r in reviews_title:
            reviews_title2.append(r.text)
        for r in reviews_body:
            reviews_body2.append(r.text)

        result = pd.DataFrame({
            "title": reviews_title2,
            "body": reviews_body2,
            "url": reviews_url,
            "photo": review_photos,
        })
        
        photo_url = result['photo'].str.split("url")
        result['photo_url'] = photo_url.str.get(1)
        result['photo_url'] = result['photo_url'].str.replace("'", "")
        result['photo_url'] = result['photo_url'].str.replace('"', "")
        result['photo_url'] = result['photo_url'].str.replace("(", "")
        result['photo_url'] = result['photo_url'].str.replace(")", "")
        result['photo_url'] = result['photo_url'].str.replace(";", "")
        result = result.drop(columns=['photo'])
        print(result)
        
        # 블로그 리뷰 몇 개 갖고올 지 정한 대로 (더보기 안누르게 해놔서 일단 5개)
        if len(reviews_title2) > BLOG_REVIEW_NUM:
            result_response = result[:BLOG_REVIEW_NUM]
        else:
            result_response = result
            
        # result_response = result_response.to_records()
        # print("************************************")
        # print(result_response)
            
        # print("========================================================",type(result_response))
        
        return Response(result_response)


class TestAPI(APIView):
    def get(self, request):
        import pandas as pd
        import numpy as np
        from tensorflow import keras
        result = {}

        # 구, 50장소 이름 받아오는 것 구현해야함
        gu = "gangnam"
        place = "가로수길"
        
        
        csv_name = f"conjest_model/seoul_test.csv"
        # csv_name = "seoul_result.csv"
        model_name1 = f"conjest_model/models_1hr/{gu}_{place}.h5"
        model_name2 = f"conjest_model/models_2hr/{gu}_{place}.h5"
        # model_name = f"gangnam_가로수길.h5"
        
        ## 예측
        df = pd.read_csv(csv_name)
        model1 = keras.models.load_model(model_name1)
        model2 = keras.models.load_model(model_name2)

        condition = df["AREA_NM"] == place
        data = df.loc[condition][["AREA_PPLTN_MIN"]].to_numpy()
        
        x_test_1hour = data[-6:].reshape(1,-1,1)
        x_test_2hour = data[-12:].reshape(1,-1,1)
        
        y_test_1hour = int(model1.predict(x_test_1hour))
        y_test_2hour = int(model2.predict(x_test_2hour))
        
        result = {
            "h_01": y_test_1hour,
            "h_02": y_test_2hour,
            "y_test_1hour" : y_test_1hour,
            "y_test_2hour" : y_test_2hour,
        }
        
        ## 혼잡도 분류
        df = pd.read_csv("conjest_model/congest_standard.csv")
        condition = df["AREA_NM"] == place
        standard1 = df.loc[condition].to_numpy()[0][-1]
        standard2 = df.loc[condition].to_numpy()[0][-2]
        for r in ["h_01","h_02"]:
            if result[r] >= standard1:
                result[r] = "혼잡"
            elif result[r] >= standard2:
                result[r] = "보통"
            else:
                result[r] = "여유"
                
        # 24시간 이전 데이터 전송
        index = []
        for i in range(24):
            index.append(-1-i*6)
        result["last_24"] = data[index].reshape(-1)
        
        return Response(result)

class TwitterAPI(APIView):
    def post(self, request):
        BEARER_TOKEN = settings.TWITTER_BEARER_TOKEN
        
        # 쿼리 받아오기
        body = json.loads(request.body)
        query = body["query"]
        print(f"쿼리 : {query}")

        response = requests.get(
            f"https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields=public_metrics,attachments&expansions=author_id,attachments.media_keys&media.fields=preview_image_url,type,url,alt_text&user.fields=name,username,profile_image_url,url",
            headers={ 
                     "Authorization": f"Bearer {BEARER_TOKEN}"
                     }
            )
        # print(response.json())
        
        return Response(response.json())