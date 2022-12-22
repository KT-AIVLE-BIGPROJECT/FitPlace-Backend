from django.contrib.auth.models import User # User 모델
from django.contrib.auth.password_validation import validate_password # 장고의 기본 패스워드 검증 도구
from django.contrib.auth import authenticate # 장고의 기본 authenticate 함수 => TokenAuth방식으로 유저를 인증해줌

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델
from rest_framework.validators import UniqueValidator # 중복 방지를 위한 검증 도구

from .models import Profile

# [회원가입 시리얼라이저]
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())], # 이메일에 대한 중복 검증
    )
    password = serializers.CharField(
        write_only=True, # 클라이언트->서버 방향의 역직렬화만 가능
        required=True,
        validators=[validate_password], # 비밀번호에 대한 형식 검증
    )
    password2 = serializers.CharField(write_only=True, required=True,)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
        return data
    
    # 유저 생성 + 토큰 생성 (create 메소드 오버라이딩)
    def create(self, validate_data):
        user = User.objects.create_user(
            username=validate_data['username'],
            email=validate_data['email'],
        )
        user.set_password(validate_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user


# [로그인 시리얼라이저] : 사용자가 ID/PW를 입력해서 보내주면 이를 확인하고 해당하는 토큰을 응답
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        user = authenticate(**data) # **: 다양한 수의 키워드 인수/매개변수 (딕셔너리 형태)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )

# [프로필 시리얼라이저]
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # "user" 필드 때문에 __all__ 못씀
        fields = ("nickname", "image", "age", "gender", "mbti", "restaurant_korea", "restaurant_west", \
                "restaurant_china", "restaurant_japan", "restaurant_fast", "restaurant_bunsik", "cafe_cafe", \
                "cafe_dessert", "cafe_bakery", "leisure_gallery", "leisure_craft", "leisure_popup", \
                "leisure_theater", "leisure_book", "leisure_department", "walking_park", "walking_market", "walking_street")