from rest_framework import serializers

from users.serializers import ProfileSerializer
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # nested serializer
    # => profile 필드에 원래는 profile의 pk값만 나타나지만 아래와 같이 시리얼라이저 안에 또다른 시리얼라이저를 넣어서
    # 이중으로 연결되는 구조로 작성해주면 해당 글 작성자의 실제 프로필 정보를 알 수 있다.
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ("pk", "profile", "title", "body", "image", "published_date", "updated_date")
    

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "body", "image")

