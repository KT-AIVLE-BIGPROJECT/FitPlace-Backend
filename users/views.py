from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import Profile

# [회원가입뷰] : 생성 기능만 있기 때문에 CreateAPIView로 간단하게
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# [로그인뷰] : 모델에 영향을 주지 않기 때문에 기본 GenericAPIView 상속
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data # validate()의 리턴값인 Token을 받아옴
        return Response({"token": token.key}, status=status.HTTP_200_OK)


# [프로필뷰] : 프로필은 보기+수정하기 두가지 기능만 필요하기 때문에 RetrieveUpdateAPIView 상속
# 프로필 수정은 로그인한 본인만 가능해야 하기 때문에 permissions.py 파일에 커스텀 권한 클래스 생성해줌
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile
    serializer_class = ProfileSerializer
    