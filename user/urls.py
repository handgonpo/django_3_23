# user/urls.py
from django.urls import path
from .views import Join, Login, LogOut, UploadProfile
from .views import edit_profile # 유저한마디
from django.contrib.auth import views as auth_views

app_name = 'user'  # 네임스페이스 지정 (템플릿이나 리다이렉션에서 'user:login' 형식으로 사용 가능)

urlpatterns = [
    path('join/', Join.as_view(), name='join'),                       # 회원가입: /user/join/
    path('login/', Login.as_view(), name='login'),                    # 로그인: /user/login/
    path('logout/', LogOut.as_view(), name='logout'),                 # 로그아웃: /user/logout/
    path('profile/upload/', UploadProfile.as_view(), name='profile_upload'),  # 프로필 이미지 업로드: /user/profile/upload/
    path('edit/', edit_profile, name='edit_profile'),  # 유저한마디: /user/edit/
]
