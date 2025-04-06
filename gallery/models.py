from django.db import models
from django.contrib.auth.models import User  # Django의 기본 User 모델


class Feed(models.Model):
    content = models.TextField()    # 글내용
    image = models.ImageField(upload_to='feeds/', default='default_feed.png')  # 피드 이미지
    email = models.EmailField(default='')     # 글쓴이
    profile_image = models.ImageField(upload_to='profiles/', default='default_profile.png')  # 프로필 이미지
    nickname = models.CharField(max_length=50, default='')  # 닉네임 (템플릿에서 필요한 것으로 보임)


class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)


class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField()


class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True)

# 새로운 프로필 모델 추가
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default_profile.png')
    nickname = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"