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


class Places(models.Model):
    place_name = models.CharField(max_length=200)
    place_photo = models.TextField()
    place_region = models.CharField(max_length=50)
    place_category = models.CharField(max_length=100)
    place_ncategory = models.CharField(max_length=100)
    place_address = models.CharField(max_length=200)
    place_street = models.CharField(max_length=100,blank=True,null=True)#가까운 장소
    place_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5.0)], default=0)
    # phoneNumberRegex = RegexValidator(regex=r'^\d{2,4}-\d{3,4}-\d{4}$')
    place_tel = models.CharField(max_length=16, blank=True, null=True)
    place_year10 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    place_year20 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    place_year30 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    place_year40 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    place_year50 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    place_year60 = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    place_male = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    place_female = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    review_summary1 = models.CharField(max_length=100)
    review_summary_cnt1 = models.IntegerField()
    review_summary2 = models.CharField(max_length=100)
    review_summary_cnt2 = models.IntegerField()
    review_summary3 = models.CharField(max_length=100)
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
    review_count = models.IntegerField()
    review_keywords = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.place_name


