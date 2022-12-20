from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# [기본 User 모델]
# username, email, password ==> 모두 required=True

# [Profile 모델]
# nickname, image, age, gender, mbti, keyword(취향)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile/', default='default.png')
    age = models.CharField(max_length=30, default="none")
    gender = models.CharField(max_length=30, default="none")
    mbti = models.CharField(max_length=30, default="none")
    
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