from uuid import uuid4
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response

from interaction.models import Like, Bookmark, Reply, Follow
from port.models import Feed


# ✅ 더 이상 사용하지 않음: get_logged_in_user()

# -------------------------------
# Main Feed View
# -------------------------------
@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class Main(APIView):
    def get(self, request):
        user = request.user

        query = request.GET.get('q', '')
        feeds = Feed.objects.filter(content__icontains=query).order_by('-id') if query else Feed.objects.all().order_by('-id')

        feed_list = []
        for feed in feeds:
            replies = Reply.objects.filter(feed=feed)
            like_count = Like.objects.filter(feed=feed, is_like=True).count()
            is_liked = Like.objects.filter(feed=feed, user=user, is_like=True).exists()
            is_marked = Bookmark.objects.filter(feed=feed, user=user, is_marked=True).exists()

            first_liker = Like.objects.filter(feed=feed, is_like=True).select_related('user__profile').first()
            first_liker_nickname = first_liker.user.profile.nickname if first_liker else "익명"

            feed_list.append({
                'id': feed.id,
                'image': feed.image,
                'content': feed.content,
                'like_count': like_count,
                'nickname': feed.user.profile.nickname,
                'profile_image': feed.user.profile.profile_image,
                'reply_list': [
                    {'nickname': reply.user.profile.nickname, 'reply_content': reply.reply_content}
                    for reply in replies
                ],
                'is_liked': is_liked,
                'is_marked': is_marked,
                'first_liker': first_liker_nickname,
            })

        recommend_users = User.objects.exclude(id=user.id).filter(profile__profile_image__isnull=False)[:5]

        return render(request, "main.html", context={
            'feeds': feed_list,
            'user': user,
            'recommend_users': recommend_users
        })


# -------------------------------
# Feed Upload View
# -------------------------------
@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(settings.MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        content = request.data.get('content')
        Feed.objects.create(
            user=request.user,
            image=uuid_name,
            content=content
        )

        return Response(status=200)


# -------------------------------
# Profile View
# -------------------------------
@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class Profile(APIView):
    def get(self, request):
        user = request.user

        # user_id가 있으면 다른 유저 프로필 보기
        user_id = request.GET.get('user_id')
        profile_user = get_object_or_404(User, id=user_id) if user_id else user

        feed_list = Feed.objects.filter(user=profile_user)
        like_feed_list = Feed.objects.filter(id__in=Like.objects.filter(user=profile_user, is_like=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=Bookmark.objects.filter(user=profile_user, is_marked=True).values_list('feed_id', flat=True))

        is_following = Follow.objects.filter(follower=user, following=profile_user).exists()

        follower_count = Follow.objects.filter(following=profile_user).count()
        following_count = Follow.objects.filter(follower=profile_user).count()

        recommend_users = User.objects.exclude(id=user.id).filter(profile__profile_image__isnull=False)[:5]

        return render(request, 'port/profile.html', {
            'feed_list': feed_list,
            'like_feed_list': like_feed_list,
            'bookmark_feed_list': bookmark_feed_list,
            'user': user,
            'profile_user': profile_user,
            'is_following': is_following,
            'follower_count': follower_count,
            'following_count': following_count,
            'recommend_users': recommend_users,
        })
