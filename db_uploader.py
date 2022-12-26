import os
import django
import csv
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitplace.settings')
django.setup()

from places.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

PLACE_PATH = 'total.csv'
SEOUL_CONGESTION = 'seoul_result.csv'


def insertPlace():
    with open(PLACE_PATH, encoding='utf-8') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            if row[0]:
                print(row[1])
                Places.objects.create(place_name=row[1], place_category=row[0], place_ncategory=row[2],
                                      place_rating=row[3],place_address=row[4], place_tel=row[5],
                                      place_year10=row[6], place_year20=row[7], place_year30=row[8],
                                      place_year40=row[9], place_year50=row[10], place_year60=row[11],
                                      place_male=row[12], place_female=row[13], place_region=row[15],place_photo=row[19],
                                      review_count=row[20],review_blog_count=row[21],
                                      review_summary1=row[22], review_summary_cnt1=float(row[23]),
                                      review_summary2=row[24], review_summary_cnt2=float(row[25]),
                                      review_summary3=row[26], review_summary_cnt3=float(row[27]),
                                      review1=row[33], review2=row[34], review3=row[35], review4=row[36],review5=row[37],
                                      review6=row[38], review7=row[39], review8=row[40], review9=row[41],review10=row[42],
                                      review_keywords=row[53],
                                      )
    print('PLACES DATA UPLOADED SUCCESSFULY!')


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
insertCongestion()
