# interaction/views.py
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Reply, Like, Bookmark
from port.models import Feed
from user.utils import get_logged_in_user
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Reply, Like, Bookmark, Follow

def get_logged_in_user(request):
    email = request.session.get('email')
    return User.objects.filter(email=email).first()


class UploadReply(APIView):
    def post(self, request):
        user = get_logged_in_user(request)
        if not user:
            return Response({'message': '로그인 필요'}, status=401)

        # request.data.get으로 feed_id와 reply_content 받아오기
        feed_id = request.data.get('feed_id')
        reply_content = request.data.get('reply_content')

        if not feed_id or not reply_content:
            return Response({'message': '필수 데이터가 누락되었습니다.'}, status=400)    

        try:
            feed = Feed.objects.get(id=feed_id)
        except Feed.DoesNotExist:
            return Response({'message': '피드를 찾을 수 없습니다.'}, status=404)

        Reply.objects.create(
            feed=feed,
            user=user,
            reply_content=reply_content
        )

        return Response({'message': '댓글이 등록되었습니다.'}, status=200)


class ToggleLike(APIView):
    def post(self, request):
        user = get_logged_in_user(request)
        if not user:
            return Response({'message': '로그인 필요'}, status=401)

        feed_id = request.data.get('feed_id')
        is_like = request.data.get('favorite_text') == 'favorite_border'

        feed = get_object_or_404(Feed, id=feed_id)
        like, _ = Like.objects.get_or_create(feed=feed, user=user)
        like.is_like = is_like
        like.save()

        # 최신 좋아요 카운트 및 첫 좋아요 유저 닉네임
        like_count = Like.objects.filter(feed=feed, is_like=True).count()
        first_liker = (
            Like.objects.filter(feed=feed, is_like=True)
            .select_related('user__profile')
            .first()
        )
        first_liker_nickname = first_liker.user.profile.nickname if first_liker else "익명"

        return Response({
            'message': '좋아요 상태 변경 완료',
            'like_count': like_count,
            'first_liker': first_liker_nickname
        }, status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        user = get_logged_in_user(request)
        if not user:
            return Response({'message': '로그인 필요'}, status=401)

        feed_id = request.data.get('feed_id')
        is_marked = request.data.get('bookmark_text') == 'bookmark_border'

        feed = get_object_or_404(Feed, id=feed_id)
        bookmark, _ = Bookmark.objects.get_or_create(feed=feed, user=user)
        bookmark.is_marked = is_marked
        bookmark.save()

        return Response({'message': '북마크 변경 완료'}, status=200)

# 팔로우 팔로잉
class ToggleFollow(APIView):
    def post(self, request):
        user = get_logged_in_user(request)

        followee_id = request.data.get('followee_id') # data.get과 Post.get의 차이점
        followee = get_object_or_404(User, id=followee_id)

        if Follow.objects.filter(follower=user, following=followee).exists():
            Follow.objects.filter(follower=user, following=followee).delete()
            is_following = False
        else:
            Follow.objects.create(follower=user, following=followee)
            is_following = True

        follower_count = Follow.objects.filter(following=followee).count()

        return Response({
            'is_following': is_following,
            'follower_count': follower_count,
        })
