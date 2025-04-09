from django.contrib import admin
from .models import Feed  # ✅ Feed만 import

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'image']
