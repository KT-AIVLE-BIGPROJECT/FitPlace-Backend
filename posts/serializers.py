from rest_framework import serializers

from users.serializers import ProfileSerializer
from .models import Post, Comment


### [ 댓글 시리얼라이저 ]
# 게시글 시리얼라이저에 댓글 시리얼라이저가 포함되기 때문에 댓글 시리얼라이저가 더 위에서 선언된다.
class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Comment
        # fields = ("pk", "profile", "post", "text")
        fields = ("pk", "profile", "post", "text", "published_date")

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "text")


### [ 게시글 시리얼라이저 ]
class PostSerializer(serializers.ModelSerializer):
    # [nested serializer]
    # => profile 필드에 원래는 profile의 pk값만 나타나지만 아래와 같이 시리얼라이저 안에 또다른 시리얼라이저를 넣어서
    # 이중으로 연결되는 구조로 작성해주면 해당 글 작성자의 실제 프로필 정보를 알 수 있다.
    profile = ProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True) # 게시글에서 댓글도 불러올 수 있도록 하기 위해 추가
    
    class Meta:
        model = Post
        fields = ("pk", "profile", "title", "body", "image", "published_date", "updated_date", "comments")
    

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "body", "image")

