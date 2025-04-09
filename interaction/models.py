from django.db import models
from django.contrib.auth.models import User
from port.models import Feed  # 외래키 참조


class Like(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('feed', 'user')

class Bookmark(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_marked = models.BooleanField(default=True)

    class Meta:
        unique_together = ('feed', 'user')

class Reply(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_content = models.TextField()   

class Follow(models.Model):
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following_set'  # 내가 팔로우한 사람들
    )
    following = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='follower_set'   # 나를 팔로우한 사람들
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"