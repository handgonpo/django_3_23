# port/urls.py
from django.urls import path
from .views import Main, UploadFeed, Profile

app_name = 'port' 

urlpatterns = [
    path('', Main.as_view(), name='main'),                  # 127.0.0.1:8000/ → Main 뷰
    path('upload', UploadFeed.as_view(), name='upload_feed'),  # 127.0.0.1:8000/upload → 피드 업로드
    path('profile', Profile.as_view(), name='profile'),     # 127.0.0.1:8000/profile → 내 프로필
]
