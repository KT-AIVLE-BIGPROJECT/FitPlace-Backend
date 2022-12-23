from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# [기본 User 모델]
# username, email, password ==> 모두 required=True

# [Profile 모델]
# nickname, image, age, gender, mbti, keyword(취향)
class Profile(models.Model):
    AGE_RANGE = [
        ('age_10', '10대'), # (db에 저장되는 값, admin이나 폼에서 표시하는 값)
        ('age_20', '20대'),
        ('age_30', '30대'),
        ('age_40', '40대'),
        ('age_50', '50대'),
        ('age_60', '60대'),
        ('age_none', '선택안함'),
    ]
    GENDER_RANGE = [
        ('gender_male', '남성'),
        ('gender_female', '여성'),
        ('gender_none', '선택안함'),
    ]
    MBTI_RANGE = [
        ('mbti_istj', 'ISTJ'),
        ('mbti_istp', 'ISTP'),
        ('mbti_isfj', 'ISFJ'),
        ('mbti_isfp', 'ISFP'),
        ('mbti_intj', 'INTJ'),
        ('mbti_intp', 'INTP'),
        ('mbti_infj', 'INFJ'),
        ('mbti_infp', 'INFP'),
        ('mbti_estj', 'ESTJ'),
        ('mbti_estp', 'ESTP'),
        ('mbti_esfj', 'ESFJ'),
        ('mbti_esfp', 'ESFP'),
        ('mbti_entj', 'ENTJ'),
        ('mbti_entp', 'ENTP'),
        ('mbti_enfj', 'ENFJ'),
        ('mbti_enfp', 'ENFP'),
        ('mbti_none', '선택안함'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile/', default='default.png')
    age = models.CharField(max_length=30, choices=AGE_RANGE, default="age_none")
    gender = models.CharField(max_length=30, choices=GENDER_RANGE, default="gender_none")
    mbti = models.CharField(max_length=30, choices=MBTI_RANGE, default="mbti_none")
    
    # 취향 설정 여부
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

# User 모델이 post_save 이벤트를 발생시켰을 때 해당 이벤트가 일어났다는 사실을 받아서,
# 해당 유저 인스턴스와 연결되는 Profile 데이터를 생성해준다.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)