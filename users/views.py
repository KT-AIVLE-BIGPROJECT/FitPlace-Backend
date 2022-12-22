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
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer 
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj




# class ProfileView(generics.GenericAPIView):
#     serializer_class = ProfileSerializer
    
#     def get(self, request):
#         profile = Profile.objects.get(user=request.user)
#         serializer = self.get_serializer(profile)
#         return Response(serializer.data)
    
#     def patch(self, request):
#         profile = Profile.objects.get(user=request.user)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data
        
#         profile.nickname = data['nickname']
#         profile.age = data['age']
#         profile.gender = data['gender']
#         profile.mbti = data['mbti']
        
#         profile.restaurant_korea = data['restaurant_korea']
#         profile.restaurant_west = data['restaurant_west']
#         profile.restaurant_china = data['restaurant_china']
#         profile.restaurant_japan = data['restaurant_japan']
#         profile.restaurant_fast = data['restaurant_fast']
#         profile.restaurant_bunsik = data['restaurant_bunsik']
        
#         profile.cafe_cafe = data['cafe_cafe']
#         profile.cafe_dessert = data['cafe_dessert']
#         profile.cafe_bakery = data['cafe_bakery']
        
#         profile.leisure_gallery = data['leisure_gallery']
#         profile.leisure_craft = data['leisure_craft']
#         profile.leisure_popup = data['leisure_popup']
#         profile.leisure_theater = data['leisure_theater']
#         profile.leisure_book = data['leisure_book']
#         profile.leisure_department = data['leisure_department']
        
#         profile.walking_park = data['walking_park']
#         profile.walking_market = data['walking_market']
#         profile.walking_street = data['walking_street']
        
#         if request.data['image']:
#             profile.image = request.data['image']
#         profile.save()
#         return Response({"result": "ok"},
#                         status=status.HTTP_206_PARTIAL_CONTENT)