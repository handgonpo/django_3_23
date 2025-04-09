# gallery_config/settings.py - 전체 프로젝트에 맞춘 최적화된 설정

from __future__ import annotations
from pathlib import Path
import os

# BASE 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 보안 관련 설정
SECRET_KEY = 'django-insecure-sebz20ftjhc=@46x$1#k+a7^l05zx#xbeck$667$+aw0nv2uet'
DEBUG = True
ALLOWED_HOSTS = ['*']

# 앱 설정
CUSTOM_APPS = [
    'user',
    'port',
    'interaction',
]

THIRD_PARTY_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
]

INSTALLED_APPS = CUSTOM_APPS + THIRD_PARTY_APPS

# 미들웨어 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # 세션 기능
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # 인증 사용자 인식
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gallery_config.urls'

# 템플릿 설정
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 전역 템플릿 디렉토리
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'gallery_config.wsgi.application'

# 데이터베이스 설정 (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 비밀번호 검증기 설정
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 국제화 설정
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# 정적 파일 (CSS, JS 등)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 미디어 파일 (업로드 이미지 등)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 기본 자동 필드
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 슬래시 자동 추가 설정 (URL 충돌 방지)
APPEND_SLASH = True

LOGIN_URL = '/user/login/' # 로그인 페이지 주소
LOGIN_REDIRECT_URL = '/user/edit/'      # 로그인 후 돌아갈 기본 주소