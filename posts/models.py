from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from users.models import Profile

# Create your models here.
class Post(models.Model):
    # related_name : User의 인스턴스로부터 user.posts.all()같은 식으로 바로 연결된 Post모델을 불러올 수 있도록 해 줄 이름
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=128)
    #category = models.CharField(max_length=128)
    body = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)