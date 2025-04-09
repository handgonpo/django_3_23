from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    사용자 확장 프로필 모델
    - Django 기본 User 모델과 1:1 관계
    - 닉네임과 프로필 이미지를 별도로 저장
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(
        upload_to='profiles/', 
        default='profiles/default_profile.png'
    )
    nickname = models.CharField(max_length=50, blank=True)
    intro_message = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def image_url(self):
        """
        템플릿에서 쉽게 이미지 URL을 사용할 수 있도록 속성 제공
        """
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        return '/media/profiles/default_profile.png'


