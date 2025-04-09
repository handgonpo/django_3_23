# port/models.py
from django.db import models
from django.contrib.auth.models import User

# 피드 게시물 모델
class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='feeds/', default='feeds/default.png')

    def __str__(self):
        return f"{self.user.username}'s post"
