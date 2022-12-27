from django.core.validators import MaxValueValidator, RegexValidator, MinValueValidator
from django.db import models


# Create your models
class Congestion(models.Model):
    area_nm = models.CharField(max_length=50)
    area_congest_lvl = models.CharField(max_length=50)
    area_ppltn_min = models.IntegerField()
    area_ppltn_max = models.IntegerField()
    now = models.DateTimeField()

    def __str__(self):
        return self.area_nm

class Place(models.Model):
    place_code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    photo = models.TextField()
    search_region = models.CharField(max_length=50)
    search_category = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    nearest_hotplace = models.CharField(max_length=100,blank=True,null=True)#가까운 장소
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5.0)], default=0)
    # phoneNumberRegex = RegexValidator(regex=r'^\d{2,4}-\d{3,4}-\d{4}$')
    tel = models.CharField(max_length=16, blank=True, null=True)
    age_10 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    age_20 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    age_30 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    age_40 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    age_50 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    age_60 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    gender_male = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    gender_female = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    mbti_is = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    mbti_in = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    mbti_es = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    mbti_en = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    review_summary1 = models.CharField(max_length=100, null=True)
    review_summary_cnt1 = models.IntegerField()
    review_summary2 = models.CharField(max_length=100, null=True)
    review_summary_cnt2 = models.IntegerField()
    review_summary3 = models.CharField(max_length=100, null=True)
    review_summary_cnt3 = models.IntegerField()
    review1 = models.TextField()
    review2 = models.TextField()
    review3 = models.TextField()
    review4 = models.TextField()
    review5 = models.TextField()
    review6 = models.TextField()
    review7 = models.TextField()
    review8 = models.TextField()
    review9 = models.TextField()
    review10 = models.TextField()
    review_blog_count = models.IntegerField()
    review_visitor_count = models.IntegerField()
    review_keywords = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class RecParam(models.Model):
    place_code = models.CharField(max_length=50)
    age_10 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    age_20 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    age_30 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    age_40 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    age_50 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    age_60 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    gender_male = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    gender_female = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    mbti_is = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    mbti_in = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    mbti_es = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    mbti_en = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    restaurant_korea = models.BooleanField(default=False)
    restaurant_west = models.BooleanField(default=False)
    restaurant_china = models.BooleanField(default=False)
    restaurant_japan = models.BooleanField(default=False)
    restaurant_fast = models.BooleanField(default=False)
    restaurant_bunsik = models.BooleanField(default=False)
    cafe_cafe = models.BooleanField(default=False)
    cafe_dessert = models.BooleanField(default=False)
    cafe_bakery = models.BooleanField(default=False)
    leisure_gallery = models.BooleanField(default=False)
    leisure_craft = models.BooleanField(default=False)
    leisure_popup = models.BooleanField(default=False)
    leisure_theater = models.BooleanField(default=False)
    leisure_book = models.BooleanField(default=False)
    leisure_department = models.BooleanField(default=False)
    walking_park = models.BooleanField(default=False)
    walking_market = models.BooleanField(default=False)
    walking_street = models.BooleanField(default=False)
    
    def __str__(self):
        return self.place_code


# class Places(models.Model):
#     place_name = models.CharField(max_length=200)
#     place_photo = models.TextField()
#     place_region = models.CharField(max_length=50)
#     place_category = models.CharField(max_length=100)
#     place_ncategory = models.CharField(max_length=100)
#     place_address = models.CharField(max_length=200)
#     place_street = models.CharField(max_length=100,blank=True,null=True)#가까운 장소
#     place_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5.0)], default=0)
#     # phoneNumberRegex = RegexValidator(regex=r'^\d{2,4}-\d{3,4}-\d{4}$')
#     place_tel = models.CharField(max_length=16, blank=True, null=True)
#     place_year10 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
#     place_year20 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
#     place_year30 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
#     place_year40 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
#     place_year50 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
#     place_year60 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
#     place_male = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
#     place_female = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
#     review_summary1 = models.CharField(max_length=100)
#     review_summary_cnt1 = models.IntegerField()
#     review_summary2 = models.CharField(max_length=100)
#     review_summary_cnt2 = models.IntegerField()
#     review_summary3 = models.CharField(max_length=100)
#     review_summary_cnt3 = models.IntegerField()
#     review1 = models.TextField()
#     review2 = models.TextField()
#     review3 = models.TextField()
#     review4 = models.TextField()
#     review5 = models.TextField()
#     review6 = models.TextField()
#     review7 = models.TextField()
#     review8 = models.TextField()
#     review9 = models.TextField()
#     review10 = models.TextField()
#     review_blog_count = models.IntegerField()
#     review_count = models.IntegerField() ###### review_visitor_count 로 바꾸기
#     review_keywords = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.place_name
