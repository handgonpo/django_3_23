from uuid import uuid4
import os

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserProfile
from .forms import UserProfileForm
from .utils import get_logged_in_user  # 공통 유틸 함수 (사용 여부 확인 필요)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt  # 개발 단계에서만 사용

# -------------------------------
# 회원가입
# -------------------------------
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        name = request.POST.get('name')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return Response(status=400, data={'message': '이미 존재하는 이메일입니다.'})

        user = User.objects.create(
            username=email,  # authenticate(username=email)과 연결됨
            email=email,
            first_name=name,
            password=make_password(password)
        )

        UserProfile.objects.create(user=user, nickname=nickname)
        return Response(status=200, data={'message': '회원가입 완료'})


# -------------------------------
# 로그인
# -------------------------------
class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.GET.get('next') or '/'

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  # Django가 세션 생성
            return redirect(next_url)
        else:
            return Response(status=400, data={'message': '회원정보가 잘못되었습니다.'})


# -------------------------------
# 로그아웃
# -------------------------------
class LogOut(APIView):
    def get(self, request):
        logout(request)  # ✅ Django 공식 로그아웃 처리
        return redirect('/user/login/')


# -------------------------------
# 프로필 이미지 업로드 (CSRF 임시 비활성화)
# -------------------------------
@method_decorator(csrf_exempt, name='dispatch')  # 개발 시만 허용, 추후 제거 권장
class UploadProfile(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        email = request.POST.get('email')

        if not file or not email:
            return Response(status=400, data={'message': '파일 또는 이메일이 누락되었습니다.'})

        uuid_name = uuid4().hex
        file_ext = file.name.split('.')[-1]
        filename = f"{uuid_name}.{file_ext}"

        save_dir = os.path.join(settings.MEDIA_ROOT, 'profiles')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        try:
            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        except Exception as e:
            return Response(status=500, data={'message': '파일 저장 중 오류', 'error': str(e)})

        try:
            user = User.objects.get(email=email)
            user_profile = user.profile
            user_profile.profile_image = f'profiles/{filename}'
            user_profile.save()
        except User.DoesNotExist:
            return Response(status=404, data={'message': '해당 이메일의 유저를 찾을 수 없습니다.'})
        except Exception as e:
            return Response(status=500, data={'message': '프로필 저장 오류', 'error': str(e)})

        return Response(status=200, data={'message': '프로필 이미지 저장 완료'})


# -------------------------------
# 프로필 수정 (한마디 포함)
# -------------------------------
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/port/profile')  # 프로필 페이지 또는 마이페이지로 이동
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user/edit_profile.html', {'form': form})
