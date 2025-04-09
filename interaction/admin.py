from django.contrib import admin
from .models import Like, Bookmark, Reply

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'feed', 'user', 'is_like']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'feed', 'user', 'is_marked']

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'feed', 'user', 'reply_content']
