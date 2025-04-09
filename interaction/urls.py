from django.urls import path
from .views import UploadReply, ToggleLike, ToggleBookmark, ToggleFollow

app_name = 'interaction'

urlpatterns = [
    path('reply', UploadReply.as_view(), name='upload_reply'),     # 댓글 등록
    path('like', ToggleLike.as_view(), name='like'),               # 좋아요 토글
    path('bookmark', ToggleBookmark.as_view(), name='bookmark'),   # 북마크 토글
    path('follow_toggle', ToggleFollow.as_view(), name='follow_toggle'),  # 팔로우 토글
]
