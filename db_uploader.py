import os
import django
import csv
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitplace.settings')
django.setup()

from places.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

# PLACE_PATH = 'total.csv'
PLACE_PATH = 'final_DBplaces_clean.csv' # 최종 장소 데이터
RECOMMEND_PARAMS_PATH = 'final_DBrecommend_params.csv' # 최종 장소 데이터들의 추천용 파라미터
SEOUL_CONGESTION = 'seoul_result.csv' # 혼잡도 데이터

# 전체 장소 데이터 DB 추가 함수
def insertPlace():
    with open(PLACE_PATH, encoding='utf-8') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            if row[0]:
                print(row[1])
                Place.objects.create(
                    place_code = row[0], name = row[1], photo = row[2], search_region = row[3], search_category = row[4],
                    category = row[5], address = row[6], nearest_hotplace = row[7], rating = row[8], tel = row[9],
                    age_10 = row[10], age_20 = row[11], age_30 = row[12], age_40 = row[13], age_50 = row[14], age_60 = row[15],
                    gender_male = row[16], gender_female = row[17], mbti_is = row[18], mbti_in = row[19], mbti_es = row[20], mbti_en = row[21],
                    review_summary1 = row[22], review_summary_cnt1 = float(row[23]), review_summary2 = row[24], review_summary_cnt2 = float(row[25]),
                    review_summary3 = row[26], review_summary_cnt3 = float(row[27]),
                    review1 = row[28], review2 = row[29], review3 = row[30], review4 = row[31], review5 = row[32], review6 = row[33],
                    review7 = row[34], review8 = row[35], review9 = row[36], review10 = row[37],
                    review_blog_count = row[38], review_visitor_count = row[39], review_keywords = row[40])
    print('PLACES DATA UPLOADED SUCCESSFULY!')

# 장소 추천 파라미터 DB 추가 함수
def insertRecParam():
    with open(RECOMMEND_PARAMS_PATH, encoding='utf-8') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        print('INSERTING RECOMMEND PARAMS DATA...')
        for row in data_reader:
            if row[0]:
                RecParam.objects.create(
                        place_code = row[0], age_10 = row[1], age_20 = row[2], age_30 = row[3], age_40 = row[4],
                        age_50 = row[5],  age_60 = row[6], gender_male = row[7], gender_female = row[8], mbti_is = row[9],
                        mbti_in = row[10], mbti_es = row[11], mbti_en = row[12], restaurant_korea = row[13],
                        restaurant_west = row[14], restaurant_china = row[15], restaurant_japan = row[16], restaurant_fast = row[17],
                        restaurant_bunsik = row[18], cafe_cafe = row[19], cafe_dessert = row[20], cafe_bakery = row[21],
                        leisure_gallery = row[22], leisure_craft = row[23], leisure_popup = row[24], leisure_theater = row[25],
                        leisure_book = row[26], leisure_department = row[27], walking_park = row[28],
                        walking_market = row[29], walking_street = row[30])
    print('RECOMMEND PARAMS DATA UPLOADED SUCCESSFULY!')

# 혼잡도 데이터 DB 추가 함수
def insertCongestion():
    with open(SEOUL_CONGESTION, encoding='utf-8') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            if row[0]:
                print(row[0])
                Congestion.objects.create(area_nm = row[0],area_congest_lvl=row[1],
                                          area_ppltn_min=row[3],area_ppltn_max=row[4],
                                          now=row[43])
    print('CONGESTION DATA UPLOADED SUCCESSFULY!')


insertPlace()
insertRecParam()
insertCongestion()




# def insertPlace():
#     with open(PLACE_PATH, encoding='utf-8') as csv_file:
#         data_reader = csv.reader(csv_file)
#         next(data_reader, None)
#         for row in data_reader:
#             if row[0]:
#                 print(row[1])
#                 Place.objects.create(place_name=row[1], place_category=row[0], place_ncategory=row[2],
#                                       place_rating=row[3],place_address=row[4], place_tel=row[5],
#                                       place_year10=row[6], place_year20=row[7], place_year30=row[8],
#                                       place_year40=row[9], place_year50=row[10], place_year60=row[11],
#                                       place_male=row[12], place_female=row[13], place_region=row[15],place_photo=row[19],
#                                       review_count=row[20],review_blog_count=row[21], ###### review_count ==> review_visitor_count 로 바꾸기
#                                       review_summary1=row[22], review_summary_cnt1=float(row[23]),
#                                       review_summary2=row[24], review_summary_cnt2=float(row[25]),
#                                       review_summary3=row[26], review_summary_cnt3=float(row[27]),
#                                       review1=row[33], review2=row[34], review3=row[35], review4=row[36],review5=row[37],
#                                       review6=row[38], review7=row[39], review8=row[40], review9=row[41],review10=row[42],
#                                       review_keywords=row[53],
#                                       )
#     print('PLACES DATA UPLOADED SUCCESSFULY!')