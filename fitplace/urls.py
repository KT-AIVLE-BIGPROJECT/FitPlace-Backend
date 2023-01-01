"""fitplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from places import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('posts.urls')),# posts.urls에 router로 이미 posts/경로 설정이 되어 있어서 여기에는 posts/ 적어주지 않음
    url('places/', views.PlaceViewSet.as_view()),
    path('recommendations/', views.RecommendationAPI.as_view()),
    path('maintoprecommend/', views.MainTopRecommendAPI.as_view()),
    path('blogreviews/', views.BlogReviewAPI.as_view()),
    url('places100/', views.PlaceTop100ViewSet.as_view()),
    url('congestion/', views.CongestionViewSet.as_view()),
    url('predictcongestion/', views.PredictCongestion.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
